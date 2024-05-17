import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from flask import Flask, request, send_file
import io
import plotly.graph_objs as go

from tensorflow.keras.models import load_model
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import preprocessing
import numpy as np

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="toxic")
    c = _conn.cursor()

    return c, _conn



# -------------------------------Registration-----------------------------------------------------------------


    


def inc_reg(username,password,email,mobile):
    try:
        c, conn = db_connect()
        print(username,password,email,mobile)
        id="0"
        status = "pending"
        j = c.execute("insert into user (id,username,password,email,mobile,status) values ('"+id +
                      "','"+username+"','"+password+"','"+email+"','"+mobile+"','"+status+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    

def fbact1(username,fb):
    try:
        c, conn = db_connect()
        print(username,fb)
        id="0"
        
        j = c.execute("insert into fb (id,username,fb) values ('"+id +
                      "','"+username+"','"+fb+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    
def editact1(username,password,email,mobile):
    try:
        c, conn = db_connect()
        print(username,password,email,mobile)
        id="0"
        
        j = c.execute("update user set password='"+password+"', email='"+email+"', mobile='"+mobile+"' where username='"+username+"'")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    
def profile_2(username):
    try:
        c, conn = db_connect()
        print(username)
        id="0"
        
        j = c.execute("update user set status='nontoxic' where username='"+username+"'")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    
def profile_4(username):
    try:
        c, conn = db_connect()
        print(username)
        id="0"
        
        j = c.execute("update user set status='all' where username='"+username+"'")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def ap_act1(username,user,post,pic,cmnt):
    try:
        c, conn = db_connect()
        print(username,user,post,pic,cmnt)
        id="0"
        status = "pending"
        model1 = load_model('toxic.h5')
        train_csv = 'train.csv'
        train_df = pd.read_csv(train_csv)
        # each toxic class is labelled as 1
        toxic_row_sums = train_df.iloc[:,2:].sum(axis=1)
        # if sum of toxic class is 0 then it is a clean comment
        train_df['clean'] = (toxic_row_sums==0)
        # Input Data
        train_texts = train_df['comment_text']
        # Output Label
        
        # set size of vocabulary
        # To Do: try different size 
        max_vocab_size = 10000
        tokenizer = Tokenizer(num_words=max_vocab_size)
        tokenizer.fit_on_texts(train_texts)
        sequences = tokenizer.texts_to_sequences(train_texts)
       # print(sequences[0])

        word_index = tokenizer.word_index
       # print('Found %s unique tokens.' % len(word_index))
        train_labels = train_df['clean']
        training_sequences = sequences[:10000]
        training_labels = train_labels[:10000]
        seq_max_len = 20
        # training padded sequences
        train_seq_pad = preprocessing.sequence.pad_sequences(sequences=training_sequences, maxlen=seq_max_len)

        # testing padded sequences
        testing_sequences = sequences[10000:11000]
        testing_labels = train_labels[10000:11000]
        test_seq_pad = preprocessing.sequence.pad_sequences(sequences=testing_sequences, maxlen=seq_max_len)

        print("fffffffffffffffffffffffffffffffff")
        test_texts = [cmnt]
        print(test_texts)
        test_sequences = tokenizer.texts_to_sequences(test_texts)
        test_seq_pad = preprocessing.sequence.pad_sequences(sequences=test_sequences, maxlen=seq_max_len)
        predictions = model1.predict(test_seq_pad, batch_size=1)
        threshold = 0.5
        binary_predictions = (predictions > threshold).astype(int)
        num_non_toxic = np.sum(binary_predictions == 1)
        num_toxic = np.sum(binary_predictions == 0)
        total_comments = len(binary_predictions)

        non_toxic_percentage = (num_non_toxic / total_comments) * 100
        toxic_percentage = (num_toxic / total_comments) * 100

        print(f"Non-Toxic Comments: {non_toxic_percentage}%")
        print(f"Toxic Comments: {toxic_percentage}%")
        pred=""        
        if binary_predictions == 1:
            status ="nontoxic"
        elif binary_predictions == 0:
            status ="toxic"

        j = c.execute("insert into Comments (id,username,user,post,pic,cmnt,status) values ('"+id +
                      "','"+username+"','"+user+"','"+post+"','"+pic+"','"+cmnt+"','"+status+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    
def ap_act(username,post,pic):
    try:
        c, conn = db_connect()
        print(username,post,pic)
        id="0"
        
        j = c.execute("insert into post (id,username,post,pic) values ('"+id +
                      "','"+username+"','"+post+"','"+pic+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

def vp():
    c, conn = db_connect()
    c.execute("select * from post ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

# def vp():
#     c, conn = db_connect()

#     c.execute("""
#         SELECT post.username, post.post, post.pic, 
#                comments.id as comment_id, comments.username AS commenter, 
#                comments.cmnt, comments.status 
#         FROM post 
#         LEFT JOIN comments ON post.pic = comments.pic 
#         ORDER BY post.pic, comments.id 
#     """)

#     result = c.fetchall()
#     conn.close()
#     return result





def vcact(user,status):
    c, conn = db_connect()
    print(status)
    status1 = 'nontoxic'
    if status==status1:
        c.execute("select * from comments where  user = '"+user+"' and status='nontoxic' ")
   
        result = c.fetchall()
        conn.close()
        print("result")
        return result
    
    else: 
        c.execute("select * from comments where user = '"+user+"'  ")
   
        result = c.fetchall()
        conn.close()
        print("result")
        return result









def vcact2(user):
    c, conn = db_connect()
    c.execute("select * from user where username = '"+user+"' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def vuact():
    c, conn = db_connect()
    c.execute("select * from user  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def vfact():
    c, conn = db_connect()
    c.execute("select * from fb  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def profile_act(username):
    c, conn = db_connect()
    c.execute("select * from user where username = '"+username+"' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


def vtcact():
    c, conn = db_connect()
    c.execute("select username,status,count(status) as scount from comments where status = 'toxic' GROUP BY username")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
# def vtcact():
#     c, conn = db_connect()
#     c.execute("select username,status,count(CASE WHEN status = 'toxic' THEN 1 END) as scount from comments GROUP BY username")
#     result = c.fetchall()
#     conn.close()
#     print("result")
#     return result


def vtcact2(username):
    c, conn = db_connect()
    c.execute("select email from user where username = '"+username+"' ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
# # -------------------------------Registration End-----------------------------------------------------------------
# # -------------------------------Loginact Start-----------------------------------------------------------------

def admin_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from admin where username='" +
                      username+"' and password='"+password+"'")
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))



def ins_loginact(username, password):
    try:
        c, conn = db_connect()
        
        j = c.execute("select * from user where username='" +
                      username+"' and password='"+password+"' "  )
        c.fetchall()
        
        conn.close()
        return j
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    print(db_connect())
