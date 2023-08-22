from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, event, html, use_state
import reactpy as rp
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


@component
def MyCrud():
    ## Creating state
    alltodo = use_state([])
    name, set_name = use_state("")
    password, set_password = use_state(0)

    def mysubmit(event):
        newtodo = {"name": name, "password": password}

        # push this to alltodo
        alltodo.set_value(alltodo.value + [newtodo])
        login(newtodo)  # function call to login function using the submitted data

    # looping data from alltodo to show on web

    list = [
        html.li(
            {
              
            },
            f"{b} => {i['name']} ; {i['password']} ",
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

uri = "mongodb+srv://root:1234@mongodblogin.pcv1to3.mongodb.net/SignUp"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["SignUp"]
collection = db["users"]
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def login(
    login_data: dict,
):  # removed async, since await makes code execution pause for the promise to resolve anyway. doesnt matter.
    username = login_data["name"]
    password = login_data["password"]

    # Create a document to insert into the collection
    document = {"name": username, "password": password}
    # logger.info('sample log message')
    print(document)

    # Insert the document into the collection
    post_id = collection.insert_one(document).inserted_id  # insert document
    print(post_id)

    return {"message": "Login successful"}


configure(app, MyCrud)