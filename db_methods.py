import sqlite3
import db_sync
import pandas as pd
import streamlit as st

def connect_db():
    """
    Connects to peckish database.
    """
    return sqlite3.connect(db_sync.get_db_path())

def create_db():
    """
    Creates aggregate cookies database if it doesn't exist.
    """
    db_sync.download_db_from_github()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS cookies (
                user TEXT,
                creation_utc TEXT,
                host_key TEXT,
                top_frame_site_key TEXT,
                name TEXT,
                path TEXT,
                expires_utc TEXT,
                is_secure TEXT,
                is_httponly TEXT,
                last_access_utc TEXT,
                has_expires TEXT,
                is_persistent TEXT,
                priority TEXT,
                samesite TEXT,
                source_scheme TEXT,
                source_port TEXT,
                last_update_utc TEXT,
                source_type TEXT,
                has_cross_site_ancestor TEXT
                ) 
            """)
    conn.commit()
    conn.close()
    db_sync.push_db_to_github()
    
def clear_db():
    """
    Resets aggregate cookies database and removes all entries.
    """
    db_sync.download_db_from_github()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cookies")
    conn.commit()
    conn.close()
    db_sync.push_db_to_github()
    
def clean_cookies(cookies: pd.DataFrame):
    """
    Removes the value and encrypted_value columns from a user's cookie for upload.
    """
    if type(cookies) != pd.DataFrame:
        print("Upload a DataFrame.")
        return None
    try:
        df = cookies.drop(["value", "encrypted_value"], axis=1)
        return df
    except Exception as e:
        try:
            df = cookies.drop(["value"], axis=1)
            return df
        except Exception as e:
            return None

def check_existing(cookies: pd.DataFrame) -> bool:
    """
    WIP.
    Checks if a user has already uploaded their cookies.
    """
    db_sync.download_db_from_github()
    conn = connect_db()
    cur = conn.cursor()

    rows = cookies.head(100)
    num = 0
    for index, _ in rows.iterrows():
        row = rows.loc[index].values.tolist()
        r = [str(r) for r in row]
        num += cur.execute("SELECT COUNT(*) FROM cookies WHERE creation_utc = ? AND host_key = ? AND expires_utc = ?", (r[0], r[1], r[5])).fetchone()[0]
    conn.close()
    if num >= 5:
        st.write("Your cookies have already been uploaded.")
        return True
    return False

def upload_cookies(username: str, cookies: pd.DataFrame):
    """
    Uploads cookies to the aggregate database.
    """
    db_sync.download_db_from_github()

    cookies_cleaned = clean_cookies(cookies)
    conn = connect_db()
    cur = conn.cursor()
    
    if not check_existing(cookies_cleaned):
        for index, _ in cookies_cleaned.iterrows():
            row = cookies_cleaned.loc[index].values.tolist()
            r = [str(r) for r in row]
            cur.execute("""INSERT INTO cookies ( user,
                        creation_utc, host_key, top_frame_site_key,
                        name, path, expires_utc, is_secure, is_httponly,
                        last_access_utc, has_expires, is_persistent,
                        priority, samesite, source_scheme, source_port,
                        last_update_utc, source_type, has_cross_site_ancestor)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """, 
                        (username, r[0], r[1], r[2],
                        r[3], r[4], r[5], r[6], r[7],
                        r[8], r[9], r[10],
                        r[11], r[12], r[13], r[14],
                        r[15], r[16], r[17])
                    )
        conn.commit()
        conn.close()
        db_sync.push_db_to_github()

def get_db() -> pd.DataFrame:
    db_sync.download_db_from_github()
    conn = connect_db()

    df = pd.read_sql_query("SELECT * FROM cookies", conn)
    conn.close()

    return df