import customtkinter
from jenkins_login import data
from Credentials import Credentials
from tkinter import ttk
from tkinter import messagebox
import os
import tkinter
from Tooltip import *
from PIL import Image
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title(" Watchguard CI Operations Center ")
root.geometry(f'{1800}*{2000}')
root.configure(background="#333333")

# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((0, 2, 3, 4, 5, 6, 7, 8), weight=0)
root.grid_rowconfigure(2, weight=1)

kind = customtkinter.StringVar()
kind.set("Username_with_password")

id = customtkinter.StringVar()
username = customtkinter.StringVar()
password = customtkinter.StringVar()
description = customtkinter.StringVar()
private_key = customtkinter.StringVar()
username_secret = customtkinter.BooleanVar()
passphrase = customtkinter.StringVar()

new_id = customtkinter.StringVar()
new_name = customtkinter.StringVar()
new_pass = customtkinter.StringVar()
new_description = customtkinter.StringVar()
new_privatekey = customtkinter.StringVar()

value1 = customtkinter.IntVar()
value2 = customtkinter.IntVar()

pod_name = customtkinter.StringVar()
pod_label = customtkinter.StringVar()
pod_usage = customtkinter.StringVar()
pod_timeout = customtkinter.StringVar()
pod_retention = customtkinter.StringVar()
pod_yaml_merge = customtkinter.StringVar()
pod_node_seelctor = customtkinter.StringVar()
pod_workspace_volume = customtkinter.StringVar()


jen_name = customtkinter.StringVar()
url = customtkinter.StringVar()
auth_username = customtkinter.StringVar()
auth_token = customtkinter.StringVar()

checkbox_index = 0
checkbox_row = 1
checkbox_variables = []
checkboxes = []


def on_checkbox_click(checkbox_index, checkbox):
    checkbox_value = checkbox_variables[checkbox_index].get()
    print(f"Checkbox {checkbox_index} clicked: {checkbox_value}")


def create_checkbox(name):
    global checkbox_index
    global checkbox_row

    checkbox_variable = customtkinter.BooleanVar()
    checkbox_variables.append(checkbox_variable)

    checkbox = customtkinter.CTkCheckBox(checkbox_slider_frame, text=name, variable=checkbox_variable,
                                         command=lambda index=checkbox_index: on_checkbox_click(checkbox_index, checkbox),
                                         font=("Helvetica", 15, "bold"),
                                         checkbox_height=20, checkbox_width=20, width=150, border_width=2,
                                         hover_color="#1F6AA4"
                                         )
    checkbox.grid(row=checkbox_row, column=0, pady=10, padx=(40, 20), sticky="nsew")
    checkboxes.append(checkbox)

    checkbox_index += 1
    checkbox_row += 1


def create_kind():
    for widgets in kind_frame.winfo_children():
        widgets.destroy()

    label = customtkinter.CTkLabel(kind_frame, text="New Credentials", font=("Helvetica", 24, "bold"))
    label.grid(row=0, column=0, pady=(5, 5), padx=(10, 2), sticky='w')

    label = customtkinter.CTkLabel(kind_frame, text="Kind", font=("Helvetica", 16, "bold"))
    label.grid(row=1, column=0, pady=5, padx=(13, 2), sticky='w')

    mbtn = customtkinter.CTkOptionMenu(master=kind_frame, variable=kind,
                                       values=["Username_with_password", "SSh_with_Private_key"],
                                       command=create_frame, font=("Helvetica", 13, "bold"), width=1000)
    mbtn.grid(row=2, column=0, padx=(10, 2), pady=(13, 0), sticky='w')


def create_submit():
    if kind.get() == "SSh_with_Private_key":
        for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):
            if boolean_element.get():
                jenkins_url = item["jenkins__url"]
                jenkins_auth_username = item["auth__username"]
                jenkins_auth_password = item["auth__password"]
                crumb_url = item["crumbIssuer"]
                obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
                response = obj.create_ssh_with_private_key(id.get(),
                                                           description.get(),
                                                           username.get(),
                                                           private_key.get(),
                                                           username_secret.get(),
                                                           crumb_url)

                if response == "Error":
                    CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                else:
                    if response.status_code == 200:
                        CTkMessagebox(title="Info", icon="check", message="Credentials created !!", font=("Helvetica", 14))
                    else:
                        CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
    else:
        for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):
            if boolean_element.get():
                jenkins_url = item["jenkins__url"]
                jenkins_auth_username = item["auth__username"]
                jenkins_auth_password = item["auth__password"]
                crumb_url = item["crumbIssuer"]
                obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
                response = obj.create_username_with_password(id.get(),
                                                             username.get(),
                                                             password.get(),
                                                             username_secret.get(),
                                                             description.get(),
                                                             crumb_url)
                # print(response)
                if response == "Error":
                    CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                else:
                    if response.status_code == 200:
                        CTkMessagebox(title="Info", icon="check", message="Credentials created !!",
                                      font=("Helvetica", 14))
                    else:
                        CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
    create_frame()

def update_test(j):
    identity = j[0]
    type = j[2]

    if type == "Username with password":
        for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):

            if boolean_element.get():
                jenkins_url = item["jenkins__url"]
                jenkins_auth_username = item["auth__username"]
                jenkins_auth_password = item["auth__password"]
                crumb_url = item["crumbIssuer"]

                obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
                response = obj.update_username_with__password(identity,
                                                              new_name.get(),
                                                              new_pass.get(),
                                                              username_secret.get(),
                                                              new_description.get(),
                                                              crumb_url
                                                              )
                if response == "Error":
                    CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                else:
                    if response.status_code == 200:
                        CTkMessagebox(title="Info", icon="check", message="Updated Successfully !!",
                                      font=("Helvetica", 14))
                    else:
                        CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)


    else:
        for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):

            if boolean_element.get():
                jenkins_url = item["jenkins__url"]
                jenkins_auth_username = item["auth__username"]
                jenkins_auth_password = item["auth__password"]
                crumb_url = item["crumbIssuer"]

                obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
                response = obj.update_ssh_with__privatekey(identity,
                                                           new_name.get(),
                                                           new_privatekey.get(),
                                                           username_secret.get(),
                                                           new_description.get(),
                                                           passphrase.get(),
                                                           crumb_url
                                                           )
                if response == "Error":
                    CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                else:
                    if response.status_code == 200:
                        CTkMessagebox(title="Info", icon="check", message="Updated Successfully !!",
                                      font=("Helvetica", 14))
                    else:
                        CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)


def delete_submit(j):
    confirmation = confirm_delete()
    if confirmation == "no":
        return

    identity = j[0]

    for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):
        if boolean_element.get():
            jenkins_url = item["jenkins__url"]
            jenkins_auth_username = item["auth__username"]
            jenkins_auth_password = item["auth__password"]
            crumb_url = item["crumbIssuer"]
            obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
            response = obj.delete(identity, crumb_url)

            print(f"response  ===== {response}")
            if response == "Error":
                CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                return
            else:
                if response:
                    if response.status_code == 200:
                        CTkMessagebox(title="Info", icon="check", message="Deleted Successfully !!",
                                      font=("Helvetica", 14))
                    else:
                        CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                        return


            print_credentials()



def create_pod_submit():
    for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):
        if boolean_element.get():
            jenkins_url = item["jenkins__url"]
            jenkins_auth_username = item["auth__username"]
            jenkins_auth_password = item["auth__password"]
            crumb_url = item["crumbIssuer"]
            obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)

            response = obj.create_pod(crumb_url=crumb_url, name=pod_name.get() , label=pod_label.get(),
                                 timeoutSeconds=pod_timeout.get())

            if response == "Error":
                CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
            else:
                if response.status_code == 200:
                    CTkMessagebox(title="Info", icon="check", message="Pod template created !!",
                                  font=("Helvetica", 14))
                else:
                    CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
    create_pod()



def multiple_functions(j):
    update_test(j)
    print_credentials()


def update_form(j):
    for widget in kind_frame.winfo_children():
        widget.destroy()

    for widget in form_frame.winfo_children():
        widget.destroy()

    identity = j[0]
    about = j[1]
    type = j[2]
    name = j[3]

    response = name

    label = customtkinter.CTkLabel(kind_frame, text="Update Credentials", font=("Helvetica", 22, "bold"), height=40)
    label.grid(row=0, column=0, pady=(5, 5), padx=(10, 2), sticky='w')

    scope_label = customtkinter.CTkLabel(master=form_frame, text="Scope", font=my_font)
    scope_label.grid(row=2, column=1, pady=(0, 0), padx=(10, 20), sticky="w")

    scope_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="GLOBAL", width=1000)
    scope_entry.grid(row=3, column=1, pady=5, padx=(10, 20), sticky="w")
    scope_entry.configure(state="readonly")
    scope_entry.insert(0, "GLOBAL")

    label = customtkinter.CTkLabel(form_frame, text="Id", font=my_font)
    label.grid(row=4, column=1, pady=5, padx=(10, 20), sticky="w")

    id_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=identity, width=1000)
    id_entry.grid(row=5, column=1, pady=5, padx=(10, 20), sticky="w")
    id_entry.focus()
    id_entry.configure(state="readonly")
    id_entry.delete(0, "end")  # Clear previous value
    id_entry.insert(0, identity)

    description_label = customtkinter.CTkLabel(form_frame, text="Description:", font=my_font)
    description_label.grid(row=6, column=1, pady=5, padx=(10, 20), sticky="w")

    description_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=about,
                                               textvariable=new_description, width=1000)
    description_entry.grid(row=7, column=1, pady=5, padx=(10, 20), sticky="w")
    description_entry.focus()
    description_entry.configure(state="normal")
    description_entry.delete(0, "end")
    description_entry.insert(0, about)

    if type == "Username with password":

        username = response.split('/')[0]
        print(username)

        username_label = customtkinter.CTkLabel(form_frame, text="Username:", font=my_font)
        username_label.grid(row=8, column=1, pady=5, padx=(10, 20), sticky="w")
        username_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=username, textvariable=new_name,
                                                width=1000)
        username_entry.grid(row=9, column=1, pady=5, padx=(10, 20), sticky="w")
        username_entry.focus()
        username_entry.delete(0, "end")
        username_entry.insert(0, username)

        checkbox = customtkinter.CTkCheckBox(master=form_frame, text="Treat username as secret",
                                             variable=username_secret,
                                             font=my_font, checkbox_height=18, checkbox_width=18, border_width=2)
        checkbox.grid(row=10, column=1, pady=5, padx=(10, 20), sticky="w")

        password_label = customtkinter.CTkLabel(form_frame, text="Password", font=my_font)
        password_label.grid(row=11, column=1, pady=5, padx=(10, 20), sticky="w")

        password_entry = customtkinter.CTkEntry(master=form_frame, width=1000, textvariable=new_pass)
        password_entry.grid(row=12, column=1, pady=5, padx=(10, 20), sticky="w")
        password_entry.focus()
        password_entry.delete(0, "end")
        password_entry.insert(0, "************")

    else:

        username = response.split(' (')[0]
        print(username)

        username_label = customtkinter.CTkLabel(form_frame, text="Username:", font=my_font)
        username_label.grid(row=8, column=1, pady=5, padx=(10, 20), sticky="w")
        username_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=username, textvariable=new_name,
                                                width=1000)
        username_entry.grid(row=9, column=1, pady=5, padx=(10, 20), sticky="w")
        username_entry.focus()
        username_entry.delete(0, "end")
        username_entry.insert(0, username)

        checkbox = customtkinter.CTkCheckBox(master=form_frame, text="Treat username as secret",
                                             variable=username_secret,
                                             font=my_font, checkbox_height=18, checkbox_width=18, border_width=2)
        checkbox.grid(row=10, column=1, pady=5, padx=(10, 20), sticky="w")

        private_key_label = customtkinter.CTkLabel(form_frame, text="Private Key", font=my_font)
        private_key_label.grid(row=11, column=1, pady=5, padx=(10, 20), sticky="w")

        private_key_entry = customtkinter.CTkEntry(master=form_frame, width=1000, placeholder_text="***************",
                                                   textvariable=new_privatekey)
        private_key_entry.grid(row=12, column=1, pady=5, padx=(10, 20), sticky="w")
        private_key_entry.focus()

        passphrase_label = customtkinter.CTkLabel(form_frame, text="Passphrase", font=my_font)
        passphrase_label.grid(row=13, column=1, pady=5, padx=(10, 20), sticky="w")

        passphrase_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="**************************",
                                                  textvariable=passphrase, width=1000)
        passphrase_entry.grid(row=14, column=1, pady=5, padx=(10, 20), sticky="w")
        passphrase_entry.focus()
        passphrase_entry.delete(0, "end")
        passphrase_entry.insert(0, "****************************************")

    submit_button = customtkinter.CTkButton(form_frame, text="Save", font=my_font,
                                            command=lambda index=identity: multiple_functions(j))
    submit_button.grid(row=15, column=1, sticky="w", padx=(10, 20), pady=5)





def confirm_delete():
    # get yes/no answers
    msg = CTkMessagebox(title="Delete ?", message=" Do you want to delete this credential ? ",
                        icon="question", option_1="No", option_2="Yes", font=("Helvetica", 14))
    response = msg.get()

    if response == "Yes":
        return "yes"
    else:
        return "no"


def create_delete_function(entry):
    def delete_entry():
        delete_submit(entry)

    return delete_entry


def create_update_function(j):
    return lambda: update_form(j)


unique_creds = set()


def print_credentials():
    global unique_creds

    for widget in kind_frame.winfo_children():
        widget.destroy()

    for widget in form_frame.winfo_children():
        widget.destroy()

    count = 0
    for i in checkbox_variables:
        if i.get() == False:
            count += 1

    if count == len(checkbox_variables):
        show_warning()
        return

    for i in checkbox_variables:
        print(i.get())

    q = 0

    labela = customtkinter.CTkLabel(kind_frame, text="Global Credentials", font=("Helvetica", 24, "bold"))
    labela.grid(row=0, column=0, pady=(20, 20), padx=(10, 2), sticky='w')

    for (jenkins_name, item), select, boolean_element in zip(data.items(), checkbox_variables, checkbox_variables):

        if boolean_element.get():

            jenkins_url = item["jenkins__url"]
            jenkins_auth_username = item["auth__username"]
            jenkins_auth_password = item["auth__password"]
            crumb_url = item["crumbIssuer"]
            obj = Credentials(jenkins_url, jenkins_auth_username, jenkins_auth_password)
            response = obj.get_credentials(crumb_url)

            if response == "Error":
                CTkMessagebox(title="Bad Request", icon="cancel", message="Request timed out", font=my_font)
                return

            credentials = response.json()["credentials"]
            unique_creds2 = set()
            for i in credentials:
                identity = i["id"]
                typename = i["typeName"]
                description = i["description"]
                username = i["displayName"]
                element = (identity, description, typename, username)

                unique_creds2.add(element)

            if len(unique_creds) == 0:
                for index in unique_creds2:
                    unique_creds.add(index)
            else:
                unique_creds = unique_creds.intersection(unique_creds2)

    q = 1

    labela = customtkinter.CTkLabel(form_frame, text="ID", font=my_font)
    labela.grid(row=q, column=0, padx=20, pady=10, sticky="w")

    labelb = customtkinter.CTkLabel(form_frame, text="Name", font=my_font)
    labelb.grid(row=q, column=1, padx=20, pady=10, sticky="w")

    labelc = customtkinter.CTkLabel(form_frame, text="Kind", font=my_font)
    labelc.grid(row=q, column=2, padx=20, pady=10, sticky="w")

    labeld = customtkinter.CTkLabel(form_frame, text="Description", font=my_font)
    labeld.grid(row=q, column=3, padx=20, pady=10, sticky="w")

    q += 1

    for j in unique_creds:

        texta = j[0]
        textb = j[1]
        textc = j[2]
        textd = j[3]

        if len(j[0]) > 15:
            texta = j[0][:10]
            texta = texta + " .."

        button = customtkinter.CTkLabel(form_frame, text=texta, font=my_font,
                                        bg_color="transparent", fg_color="transparent", anchor="w"
                                        )
        button.grid(row=q, column=0, padx=20, pady=5, sticky="w")
        CreateToolTip(button, j[0])

        if len(j[3]) > 15:
            textd = j[3][:10]
            textd = textd + " .."

        label2 = customtkinter.CTkLabel(form_frame, text=textd, font=my_font)
        label2.grid(row=q, column=1, padx=20, pady=5, sticky="w")
        CreateToolTip(label2, j[3])

        if len(j[2]) > 15:
            textc = j[2][:10]
            textc = textc + " .."

        label3 = customtkinter.CTkLabel(form_frame, text=textc, font=my_font)
        label3.grid(row=q, column=2, padx=20, pady=5, sticky="w")
        CreateToolTip(label3, j[2])


        if len(j[1]) > 15:
            textb = j[1][:10]
            textb = textb + " .."

        label4 = customtkinter.CTkLabel(form_frame, text=textb, font=my_font)
        label4.grid(row=q, column=3, padx=20, pady=5, sticky="w")
        CreateToolTip(label4, j[1])

        button1 = customtkinter.CTkButton(
            form_frame,
            text="Update",
            font=my_font,
            command=create_update_function(j),
            text_color="white"
        )
        button1.grid(row=q, column=5, padx=(20, 20), pady=5, sticky="e")

        button2 = customtkinter.CTkButton(
            form_frame,
            text="Delete",
            font=my_font,
            command=create_delete_function(j),
            text_color="white"
        )
        button2.grid(row=q, column=6, padx=(10, 10), pady=5, sticky="e")

        q += 1
    unique_creds.clear()


def pod_select_alert():
    count = 0
    for i in checkbox_variables:
        if i.get() == False:
            count += 1

    if count == len(checkbox_variables):
        show_warning()
        return

    create_pod()

def add_credentials_frame():
    count = 0
    for i in checkbox_variables:
        if i.get() == False:
            count += 1

    if count == len(checkbox_variables):
        show_warning()
        return
    create_kind()
    create_frame()


def display():
    label = customtkinter.CTkLabel(details_frame, text=kind.get())
    label.grid()


def show_warning():
    # Show some retry/cancel warnings
    msg = CTkMessagebox(title="Warning Message !", message=" Please Select a Jenkins-Controller !! ",
                        icon="warning", option_1="OK", font=("Helvetica", 14))


def create_frame():
    print(checkbox_variables)

    id.set("")
    username.set(" ")
    password.set(" ")
    description.set(" ")
    private_key.set(" ")
    username_secret.set(False)
    passphrase.set(" ")

    for widget in form_frame.winfo_children():
        widget.destroy()

    scope_label = customtkinter.CTkLabel(master=form_frame, text="Scope", font=my_font)
    scope_label.grid(row=2, column=1, pady=(10, 0), padx=(10, 20), sticky="w")

    scope_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="GLOBAL", width=1000)
    scope_entry.grid(row=3, column=1, pady=5, padx=(10, 20), sticky="w")
    scope_entry.configure(state="readonly")
    scope_entry.insert(0, "GLOBAL")

    label = customtkinter.CTkLabel(form_frame, text="Id", font=my_font)
    label.grid(row=4, column=1, pady=5, padx=(10, 20), sticky="w")

    id_entry = customtkinter.CTkEntry(master=form_frame, textvariable=id, placeholder_text="Id", width=1000)
    id_entry.grid(row=5, column=1, pady=5, padx=(10, 20), sticky="w")
    id_entry.focus()

    description_label = customtkinter.CTkLabel(form_frame, text="Description:", font=my_font)
    description_label.grid(row=6, column=1, pady=5, padx=(10, 20), sticky="w")
    description_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="description",
                                               textvariable=description, width=1000)
    description_entry.grid(row=7, column=1, pady=5, padx=(10, 20), sticky="w")
    description_entry.focus()

    username_label = customtkinter.CTkLabel(form_frame, text="Username:", font=my_font)
    username_label.grid(row=8, column=1, pady=5, padx=(10, 20), sticky="w")
    username_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Username", textvariable=username,
                                            width=1000)
    username_entry.grid(row=9, column=1, pady=5, padx=(10, 20), sticky="w")
    username_entry.focus()

    checkbox = customtkinter.CTkCheckBox(master=form_frame, text="Treat username as secret", variable=username_secret,
                                         font=my_font, checkbox_height=18, checkbox_width=18, border_width=2)
    checkbox.grid(row=10, column=1, pady=5, padx=(10, 20), sticky="w")

    if kind.get() == "Username_with_password":

        password_label = customtkinter.CTkLabel(form_frame, text="Password", font=my_font)
        password_label.grid(row=11, column=1, pady=5, padx=(10, 20), sticky="w")

        password_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Password",
                                                textvariable=password, width=1000)
        password_entry.grid(row=12, column=1, pady=5, padx=(10, 20), sticky="w")
        password_entry.focus()

        submit_button = customtkinter.CTkButton(master=form_frame, text="Create",
                                                command=create_submit, font=my_font)
        submit_button.grid(row=13, column=1, pady=5, padx=(10, 20), sticky="w")

    else:

        private_key_label = customtkinter.CTkLabel(form_frame, text="Private Key", font=("Helvetica", 10))
        private_key_label.grid(row=11, column=1, pady=5, padx=(10, 20), sticky="w")

        private_key_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=" Privatekey ",
                                                   textvariable=private_key, width=1000)
        private_key_entry.grid(row=12, column=1, pady=5, padx=(10, 20), sticky="w")
        private_key_entry.focus()

        passphrase_label = customtkinter.CTkLabel(form_frame, text="Passphrase", font=my_font)
        passphrase_label.grid(row=13, column=1, pady=5, padx=(10, 20), sticky="w")

        passphrase_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text=" Privatekey ",
                                                  textvariable=passphrase, width=1000)
        passphrase_entry.grid(row=14, column=1, pady=5, padx=(10, 20), sticky="w")
        passphrase_entry.focus()

        submit_button = customtkinter.CTkButton(master=form_frame, text="Create",
                                                command=create_submit, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=15, column=1, pady=5, padx=(10, 20), sticky="w")


place = 0


def add_volume_form():

    form_frame3 = customtkinter.CTkFrame(form_frame, height=10, width=100, bg_color="transparent",
                                         fg_color="transparent",border_width=2)
    form_frame3.grid(row=11, column=1, padx=(5, 5), pady=(10, 10), sticky="nsew")

    for widget in form_frame3.winfo_children():
        widget.destroy()

    place = 0

    label = customtkinter.CTkLabel(form_frame3, text="Add Volume", font=("Helvetica", 20, "bold"))
    label.grid(row=0, column=1, pady=(20, 0), padx=(20, 20), sticky='nsew')
    place += 1

    name_label = customtkinter.CTkLabel(master=form_frame3, text="Config Map name", font=my_font)
    name_label.grid(row=1, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    name_entry = customtkinter.CTkEntry(master=form_frame3, placeholder_text="Name", width=1000)
    name_entry.grid(row=2, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    dockerimg_label = customtkinter.CTkLabel(master=form_frame3, text="Mount Path", font=my_font)
    dockerimg_label.grid(row=3, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    dockerimg_entry = customtkinter.CTkEntry(master=form_frame3, placeholder_text="Name", width=1000)
    dockerimg_entry.grid(row=4, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1


def add_container_form():

    form_frame2 = customtkinter.CTkFrame(form_frame, height=10, width=100, bg_color="transparent",
                                         fg_color="transparent" , border_width=2)
    form_frame2.grid(row=9, column=1, padx=(5, 5), pady=(10, 10), sticky="nsew")
    place = 0

    for widget in form_frame2.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(form_frame2, text="Add Container", font=("Helvetica", 20, "bold"))
    label.grid(row=place, column=1, pady=(20, 0), padx=(20, 20), sticky='nsew')
    place += 1

    name_label = customtkinter.CTkLabel(master=form_frame2, text="Name", font=my_font)
    name_label.grid(row=place, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    name_entry = customtkinter.CTkEntry(master=form_frame2, placeholder_text="Name", width=1000)
    name_entry.grid(row=place, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    dockerimg_label = customtkinter.CTkLabel(master=form_frame2, text="Docker Image", font=my_font)
    dockerimg_label.grid(row=place, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    dockerimg_entry = customtkinter.CTkEntry(master=form_frame2, placeholder_text="Name", width=1000)
    dockerimg_entry.grid(row=place, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    workingdir_label = customtkinter.CTkLabel(master=form_frame2, text="Working Directory", font=my_font)
    workingdir_label.grid(row=place, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    workingdir_entry = customtkinter.CTkEntry(master=form_frame2, placeholder_text="Name", width=1000)
    workingdir_entry.grid(row=place, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    command_label = customtkinter.CTkLabel(master=form_frame2, text="Command to run", font=my_font)
    command_label.grid(row=place, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    command_entry = customtkinter.CTkEntry(master=form_frame2, placeholder_text="", width=1000)
    command_entry.grid(row=place, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    arg_label = customtkinter.CTkLabel(master=form_frame2, text="Arguments to pass to the command", font=my_font)
    arg_label.grid(row=place, column=1, pady=(0, 0), padx=(10, 20), sticky="w")
    place += 1

    arg_entry = customtkinter.CTkEntry(master=form_frame2, placeholder_text="Name", width=1000)
    arg_entry.grid(row=place, column=1, pady=5, padx=(10, 20), sticky="w")
    place += 1

    checkbox = customtkinter.CTkCheckBox(master=form_frame2, text="Allocate pseudo TTY")
    checkbox.grid(row=place, column=1, pady=5, padx=(10,10), sticky="w")




def create_pod():

    global place
    pod_name.set(" ")
    pod_label.set(" ")
    pod_usage.set(" ")
    pod_timeout.set(" ")
    pod_retention.set(" ")
    pod_yaml_merge.set(" ")
    pod_node_seelctor.set(" ")
    pod_workspace_volume.set(" ")
    pod_usage.set("Use this node as much as possible")


    for widget in kind_frame.winfo_children():
        widget.destroy()

    for widget in form_frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(kind_frame, text="Pod Template", font=("Helvetica", 20, "bold"))
    label.grid(row=0, column=1, pady=(0, 0), padx=(10, 20), sticky='w')
    place += 1

    name_label = customtkinter.CTkLabel(master=form_frame, text="Name", font=my_font)
    name_label.grid(row=0, column=1, pady=5, padx=(10, 20), sticky="w")

    name_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Name", width=1000, textvariable=pod_name)
    name_entry.grid(row=1, column=1, pady=5, padx=(10, 20), sticky="w")

    labeldetails = customtkinter.CTkLabel(form_frame, text="Pod Template details", font=("Helvetica", 13, "bold"))
    labeldetails.grid(row=2, column=1, pady=5, padx=(13, 20), sticky='w')

    label = customtkinter.CTkLabel(form_frame, text="Label", font=my_font)
    label.grid(row=4, column=1, pady=5, padx=(20, 20), sticky="w")

    id_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Label", textvariable=pod_label, width=1000)
    id_entry.grid(row=5, column=1, pady=5, padx=(20, 20), sticky="w")
    id_entry.focus()

    label = customtkinter.CTkLabel(form_frame, text="Usage", font=my_font)
    label.grid(row=6, column=1, pady=5, padx=(20, 20), sticky="w")

    mbtn = customtkinter.CTkOptionMenu(master=form_frame,
                                       values=["Use this node as much as possible",
                                               "Only build jobs with label expressions matching this node "],
                                       variable=pod_usage,
                                       font=my_font,width=1000
                                       )
    mbtn.grid(row=7, column=1, pady=5, padx=(20, 20), sticky="w")
    mbtn.set("Use this node as much as possible")

    container_add_button = customtkinter.CTkButton(form_frame, text="Add Container", font=my_font,
                                                   command=add_container_form)
    container_add_button.grid(row=8, column=1, pady=(20,5), padx=(20, 20), sticky="w")


    volume_add_button = customtkinter.CTkButton(form_frame, text="Add Volume", font=my_font,
                                                command=add_volume_form)
    volume_add_button.grid(row=10, column=1, pady=(10,5), padx=(20, 20), sticky="w")

    workingdir_label = customtkinter.CTkLabel(master=form_frame, text="Pod Retention", font=my_font)
    workingdir_label.grid(row=12, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    mbtn2 = customtkinter.CTkOptionMenu(master=form_frame,
                                        values=["Always","Default","Never","On Failure"],
                                        variable=pod_retention,
                                        font=my_font, width=1000
                                        )
    mbtn2.grid(row=13, column=1, pady=5, padx=(20, 20), sticky="w")
    mbtn2.set("Default")

    command_label = customtkinter.CTkLabel(master=form_frame, text="Timeout in seconds for Jenkins connection",
                                           font=my_font)
    command_label.grid(row=14, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    command_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="", width=1000, textvariable=pod_timeout)
    command_entry.grid(row=15, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    arg_label = customtkinter.CTkLabel(master=form_frame, text="Yaml merge strategy", font=my_font)
    arg_label.grid(row=16, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    mbtn3 = customtkinter.CTkOptionMenu(master=form_frame, button_color="#333333",
                                       values=["Override","Merge"],
                                       font=my_font, width=1000,
                                       variable=pod_yaml_merge
                                       )
    mbtn3.grid(row=17, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    mbtn3.set("Override")

    node_selector_label = customtkinter.CTkLabel(master=form_frame, text="Node selector", font=my_font)
    node_selector_label.grid(row=19, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    node_selector_entry = customtkinter.CTkEntry(master=form_frame,textvariable=pod_node_seelctor, placeholder_text="Name", width=1000)
    node_selector_entry.grid(row=20, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    workspace_volume_label = customtkinter.CTkLabel(master=form_frame, text="Workspace Volume", font=my_font)
    workspace_volume_label.grid(row=21, column=1, pady=(10,5), padx=(20, 20), sticky="w")
    place += 1

    mbtn4 = customtkinter.CTkOptionMenu(master=form_frame, button_color="#333333",
                                        values=[
                                            "Empty Dir workspace Volume",
                                            "Dynamic Persistent volume claim",
                                            "Host path workspace volume",
                                            "NFS Workspace Volume",
                                            "Persistent Volume Claim Workspace Volume"
                                                ],
                                        font=my_font, width=1000,
                                        variable=pod_workspace_volume
                                        )
    mbtn4.grid(row=22, column=1, pady=(10, 5), padx=(20, 20), sticky="w")
    mbtn4.set("Empty Dir workspace Volume")

    submit_button = customtkinter.CTkButton(master=form_frame, text="Submit", font=my_font, command=create_pod_submit)
    submit_button.grid(row=23, column=1, pady=(10,5), padx=(20, 20), sticky="w")


my_font = customtkinter.CTkFont(family="Helvetica", size=16)

# Frames for window

sidebar_frame = customtkinter.CTkFrame(root, width=165, corner_radius=0)
sidebar_frame.grid(row=0, column=0, padx=(5, 5), pady=20, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure((3, 4), weight=1)

options_frame = customtkinter.CTkFrame(sidebar_frame, width=140, height=50, corner_radius=5,
                                       border_width=0)
options_frame.grid(row=1, column=0, sticky="n", pady=(12, 0))
options_frame.grid_rowconfigure((3, 4), weight=1)

main_frame = customtkinter.CTkFrame(root, height=600, width=1200, border_width=0, border_color="#F4F3F8",
                                    bg_color="transparent")
main_frame.grid(row=1, column=1, padx=0, pady=(25, 20), sticky="w")
main_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

checkbox_slider_frame = customtkinter.CTkScrollableFrame(main_frame, height=280, width=200, bg_color="transparent")
checkbox_slider_frame.grid(row=1, column=1, padx=2, pady=(2, 0), sticky="nw")

checkbox_slider_frame.grid_rowconfigure((0, 1, 2), weight=1)
checkbox_slider_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

details_frame = customtkinter.CTkScrollableFrame(main_frame, height=600, width=1200, bg_color="transparent")
details_frame.grid(row=1, column=1, padx=(220, 2), pady=(2, 0), sticky="nw")
details_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
details_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

sidebar_button_0 = customtkinter.CTkButton(options_frame, text="Manage Credentials", text_color="white",
                                           font=my_font, state="Disabled")
sidebar_button_0.grid(row=2, column=0, padx=20, pady=(30, 10))

sidebar_button_1 = customtkinter.CTkButton(options_frame, text="Add Credentials", font=my_font,
                                           command=add_credentials_frame, fg_color="transparent", hover_color="#1F6AA4")
sidebar_button_1.grid(row=3, column=0, padx=(40, 20), pady=(5, 10))

sidebar_button_2 = customtkinter.CTkButton(options_frame, text="Get Credentials", font=my_font,
                                           command=print_credentials, fg_color="transparent", hover_color="#1F6AA4")
sidebar_button_2.grid(row=4, column=0, padx=(40, 20), pady=(5, 10))

sidebar_button_3 = customtkinter.CTkButton(options_frame, text="Manage Pods", text_color="white",
                                           font=my_font, state="Disabled")
sidebar_button_3.grid(row=5, column=0, padx=20, pady=(15, 10))

sidebar_button_4 = customtkinter.CTkButton(options_frame, text="Add Pods", font=my_font,
                                           command=pod_select_alert, fg_color="transparent", hover_color="#1F6AA4")
sidebar_button_4.grid(row=6, column=0, padx=(40, 20), pady=(5, 10), sticky="e")

title_frame = customtkinter.CTkFrame(root, height=100, width=150, border_width=0, bg_color="transparent",
                                     fg_color="transparent")
title_frame.grid(row=0, column=1, padx=(20, 20), pady=(40, 30), sticky="nsew")
title_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

logo_label = customtkinter.CTkLabel(master=title_frame, text="WG CI-OperationsCenter",
                                    font=("Helvetica", 32, "bold"))
logo_label.grid(row=0, column=0, padx=(400, 200), pady=(20, 10))

# kind and form frame
kind_frame = customtkinter.CTkFrame(details_frame, height=10, width=250, bg_color="transparent",
                                    fg_color="transparent")
kind_frame.grid(row=0, column=0, padx=(50, 0), pady=(0, 0), sticky="nsew")

form_frame = customtkinter.CTkFrame(details_frame, height=10, width=250, bg_color="transparent",
                                    fg_color="transparent",border_color="yellow",border_width=0)
form_frame.grid(row=1, column=0, padx=(50, 5), pady=(0, 0), sticky="nsew")

checkbox_slider_frame.grid_rowconfigure(1, weight=1)

allselect = customtkinter.BooleanVar()

# Insert Image
IMAGE_WIDTH = 70
IMAGE_HEIGHT = 100
IMAGE_PATH = '1200px-Jenkins_logo.svg.png'

your_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
label = customtkinter.CTkLabel(master=sidebar_frame, image=your_image, text='')
label.grid(column=0, row=0, pady=(30, 0), padx=5)


def operation():
    if allselect.get():
        for var in checkbox_variables:
            var.set(True)
    else:
        for var in checkbox_variables:
            var.set(False)


def select_all():
    checkbox = customtkinter.CTkCheckBox(checkbox_slider_frame, text="  Select All", variable=allselect,
                                         command=operation,
                                         font=("Helvetica", 15, "bold"),
                                         checkbox_height=20, checkbox_width=20, width=150, border_width=2,
                                         hover_color="#1F6AA4"
                                         )
    checkbox.grid(row=0, column=0, pady=10, padx=(40, 30), sticky="nsew")


def start():
    for jenkins_name in data:
        print(jenkins_name)
        create_checkbox(jenkins_name)


select_all()
start()

root.mainloop()
