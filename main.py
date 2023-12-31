from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state
import reactpy as rp
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient



@component
def MyCrud():
    ## creating state
    alltodo  = use_state([])
    name,set_name = use_state ("")
    password,set_password = use_state(0)

    def mysubmit(event):
        newtodo = {"name": name, "password": password}

        #push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)

#looping data from alltodo to show on web
    
    list = [
        html.li(
            {


            },
            f"{b} => {i['name']} ; {i['password']}",
        )
        for b, i in enumerate(alltodo.value)
    ]   

    def handle_event(event):
        print(event)
    
    return html.div(
        {"style": {"padding": "10px"}},
        ## creating form for submission\
        html.form(
            {"on submit": mysubmit},
            html.h1("Login Form - ReactPy & Mongodb"),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "test",
                    "placeholder": "Password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            # creating submit button on form
            html.button(
                {
                    "type": "submit",
                    "on_click": event(
                        lambda event: mysubmit(event), prevent_default=True
                    ),
                },
                "Submit",
            ),
        ),
        html.ul(list),
    )


app = FastAPI()
    
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#COPY AND PASTING THE MONGODB URI.
uri = "mongodb+srv://admin:admin123@cluster0.ksvd0uq.mongodb.net/"
Client = MongoClient(uri, Server_Api=ServerApi("1"))

#defining the db name
db = Client ["DB"]
collection = db["Reactpy"]

#checking the connection
try: 
    Client .admin.command("Ping")
    print("Pinged your deployment. You Sucessfully Connected to MongoDB")
except Exception as e:
    print (e)

def login(
        login_data: dict,
):#resolved async, since  
    username = login_data("name")
    password = login_data("password")

    #create a document to insert into the collection
    document = {"name": username, "password": password}
    #logger.info("sample log message")
    print(document)

    #insert the document into the collection
    post_id = collection.insert_one(document).inserted_id #insert document
    print(post_id)

    return{"message":"Login Sucessful"}

configure(app, MyCrud)