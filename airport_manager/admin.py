import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser

import pymysql
from pymysql.err import OperationalError

from fids_common import settings, login, reportgen

class DataFrame(tk.Frame):
    def __init__(self, parent, con, query=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # initialize parent tk

        self.__con = con
        self._parent = parent

        if query:
            self._sql_query = query
        else:
            self._sql_query = "SELECT `id`, `ifid`, `ofid`, `from`, `to`, `sta`, `eta`, `std`, `etd`, `checkinctr`, `status`, `beltstatus`, `gate`, `belt` FROM `flight`;"
        
        # Table adding
        self.__heading_1 = tk.Label(self, text="Incoming Flight ID")
        self.__heading_1.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_2 = tk.Label(self, text="Outgoing Flight ID")
        self.__heading_2.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_3 = tk.Label(self, text="From")
        self.__heading_3.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_4 = tk.Label(self, text="To")
        self.__heading_4.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_5 = tk.Label(self, text="STA")
        self.__heading_5.grid(row=0, column=4, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_6 = tk.Label(self, text="ETA")
        self.__heading_6.grid(row=0, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_7 = tk.Label(self, text="STD")
        self.__heading_7.grid(row=0, column=6, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_8 = tk.Label(self, text="ETD")
        self.__heading_8.grid(row=0, column=7, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_9 = tk.Label(self, text="Check-in counter")
        self.__heading_9.grid(row=0, column=8, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_10 = tk.Label(self, text="Status")
        self.__heading_10.grid(row=0, column=9, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_11 = tk.Label(self, text="Belt status")
        self.__heading_11.grid(row=0, column=10, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_12 = tk.Label(self, text="Gate")
        self.__heading_12.grid(row=0, column=11, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_13 = tk.Label(self, text="Belt")
        self.__heading_13.grid(row=0, column=12, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_14 = tk.Label(self, text="Edit")
        self.__heading_14.grid(row=0, column=13, sticky=tk.N + tk.S + tk.E + tk.W)
        self.__heading_15 = tk.Label(self, text="Delete")
        self.__heading_15.grid(row=0, column=14, sticky=tk.N + tk.S + tk.E + tk.W)

        for i in range(15):
            tk.Grid.columnconfigure(self, i, weight=1)

        cur = self.__con.cursor()
        cur.execute(
            "SELECT `id`, `ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
            " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
            "`gate`, `belt` FROM `flight`;"
        )

        i = 1

        self.__matrix = []

        for data in cur.fetchall():
            l1 = tk.Label(self, text=data[1])
            l1.grid(row=i, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
            l2 = tk.Label(self, text=data[2])
            l2.grid(row=i, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

            l3 = tk.Label(self, text=data[3])
            l3.grid(row=i, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

            l4 = tk.Label(self, text=data[4])
            l4.grid(row=i, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
            l5 = tk.Label(self, text=data[5])
            l5.grid(row=i, column=4, sticky=tk.N + tk.S + tk.E + tk.W)

            l6 = tk.Label(self, text=data[6])
            l6.grid(row=i, column=5, sticky=tk.N + tk.S + tk.E + tk.W)
            l7 = tk.Label(self, text=data[7])
            l7.grid(row=i, column=6, sticky=tk.N + tk.S + tk.E + tk.W)
            l8 = tk.Label(self, text=data[8])
            l8.grid(row=i, column=7, sticky=tk.N + tk.S + tk.E + tk.W)

            l9 = tk.Label(self, text=data[9])
            l9.grid(row=i, column=8, sticky=tk.N + tk.S + tk.E + tk.W)
            l10 = tk.Label(self, text=data[10])
            l10.grid(row=i, column=9, sticky=tk.N + tk.S + tk.E + tk.W)
            l11 = tk.Label(self, text=data[11])
            l11.grid(row=i, column=10, sticky=tk.N + tk.S + tk.E + tk.W)

            l12 = tk.Label(self, text=data[12])
            l12.grid(row=i, column=11, sticky=tk.N + tk.S + tk.E + tk.W)
            l13 = tk.Label(self, text=data[13])
            l13.grid(row=i, column=12, sticky=tk.N + tk.S + tk.E + tk.W)

            def __edit(idd=data[0]):
                EditFlightWindow(self._parent, self.__con, idd)

            def __delete(idd=data[0]):
                cur = self.__con.cursor()
                cur.execute("DELETE FROM `flight` WHERE id = %(id)s", {"id": idd})
                # if messagebox.askyesno("Delete", "Delete?") == "yes":
                self.__con.commit()
                cur.close()
                self._parent._refresh_table()

            b14 = ttk.Button(self, text="Edit", command=__edit)
            b14.grid(row=i, column=13, sticky=tk.N + tk.S + tk.E + tk.W)
            b15 = ttk.Button(self, text="Delete", command=__delete)
            b15.grid(row=i, column=14, sticky=tk.N + tk.S + tk.E + tk.W)

            i += 1

        cur.close()


class HomeScreen(tk.Tk):
    def __init__(self, con, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk

        self.title("User home")
        self.__con = con

        self.__logout_btn = tk.Label(self, text="Welcome to FIDS")
        self.__logout_btn.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.__menu = tk.Menu(self)

        self.__user_menu = tk.Menu(self.__menu, tearoff=0)
        self.__user_menu.add_command(label="Logout", command=self.__logout)

        self.__menu.add_cascade(label="User", menu=self.__user_menu)

        self.__flight_menu = tk.Menu(self.__menu, tearoff=0)
        self.__flight_menu.add_command(label="Add", command=self.__addflight)
        self.__flight_menu.add_command(label="Edit", command=None)
        self.__flight_menu.add_command(label="Delete", command=None)
        self.__flight_menu.add_separator()
        self.__flight_menu.add_command(
            label="Refresh Table", command=self._refresh_table
        )
        self.__flight_menu.add_command(
            label="Delay Report", command=self._delayreport
        )

        self.__menu.add_cascade(label="Flight", menu=self.__flight_menu)

        self.config(menu=self.__menu)

        self.__dframe = DataFrame(self, self.__con)
        self.__dframe.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Grid.columnconfigure(self, 0, weight=1)
        
    def _delayreport(self):
        reportgen.ReportPDF(self.__con, orientation="landscape").delay_report("report.pdf") 
        webbrowser.open_new("report.pdf")

    def __logout(self):
        self.__con.close()
        self.destroy()

    def __addflight(self):
        AddFlightWindow(self, self.__con)

    def __print(self):
        print("Hii")

    def __msgbox(self, plug):
        print("The user has", plug)

    def _refresh_table(self):
        self.__dframe.destroy()
        self.__dframe = DataFrame(self, self.__con)
        self.__dframe.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)


class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk

        self.title("User sign in")

        # host
        self.__host_label = tk.Label(self, text="Host:")
        self.__host_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self.__host_entry = ttk.Entry(self)
        self.__host_entry.grid(column=1, row=0, sticky=tk.E, padx=10, pady=10)

        # username
        self.__username_label = tk.Label(self, text="Username:")
        self.__username_label.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.__username_entry = ttk.Entry(self)
        self.__username_entry.grid(column=1, row=1, sticky=tk.E, padx=10, pady=10)

        # password
        self.__password_label = tk.Label(self, text="Password:")
        self.__password_label.grid(column=0, row=2, sticky=tk.W, padx=10, pady=5)

        self.__password_entry = ttk.Entry(self, show="*")
        self.__password_entry.grid(column=1, row=2, sticky=tk.E, padx=10, pady=5)

        # database
        self.__db_label = tk.Label(self, text="Database:")
        self.__db_label.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        self.__db_entry = ttk.Entry(self)
        self.__db_entry.grid(column=1, row=3, sticky=tk.E, padx=10, pady=10)

        # login button
        self.__login_button = ttk.Button(self, text="Login", command=self.__login)
        self.__login_button.grid(column=1, row=4, sticky=tk.S, padx=5, pady=5)

    def __login(self):
        try:
            h = self.__host_entry.get()
            u = self.__username_entry.get()
            p = self.__password_entry.get()
            d = self.__db_entry.get()
            con = pymysql.connect(host=h, user=u, password=p, database=d)
        except OperationalError as e:
            messagebox.showerror(str(type(e)), str(e))
        else:
            HomeScreen(con)

            self.destroy()


"""
`ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
                    " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
                    "`gate`, `belt` FROM `flight`;")
"""


class FlightWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize parent tk

        # self.title("Edit Flight")

        self._ifid_label = tk.Label(self, text="Incoming Flight ID:")
        self._ifid_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        self._ifid_entry = ttk.Entry(self)
        self._ifid_entry.grid(column=1, row=0, sticky=tk.E, padx=10, pady=10)

        self._ofid_label = tk.Label(self, text="Outgoing Flight ID:")
        self._ofid_label.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self._ofid_entry = ttk.Entry(self)
        self._ofid_entry.grid(column=1, row=1, sticky=tk.E, padx=10, pady=10)

        self._from_label = tk.Label(self, text="From:")
        self._from_label.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self._from_entry = ttk.Entry(self)
        self._from_entry.grid(column=1, row=2, sticky=tk.E, padx=10, pady=10)

        self._to_label = tk.Label(self, text="To:")
        self._to_label.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        self._to_entry = ttk.Entry(self)
        self._to_entry.grid(column=1, row=3, sticky=tk.E, padx=10, pady=10)

        self._sta_label = tk.Label(self, text="STA:")
        self._sta_label.grid(column=0, row=4, sticky=tk.W, padx=10, pady=10)

        self._sta_entry = ttk.Entry(self)
        self._sta_entry.grid(column=1, row=4, sticky=tk.E, padx=10, pady=10)

        self._eta_label = tk.Label(self, text="ETA:")
        self._eta_label.grid(column=0, row=5, sticky=tk.W, padx=10, pady=10)

        self._eta_entry = ttk.Entry(self)
        self._eta_entry.grid(column=1, row=5, sticky=tk.E, padx=10, pady=10)

        self._std_label = tk.Label(self, text="STD:")
        self._std_label.grid(column=0, row=6, sticky=tk.W, padx=10, pady=10)

        self._std_entry = ttk.Entry(self)
        self._std_entry.grid(column=1, row=6, sticky=tk.E, padx=10, pady=10)

        self._etd_label = tk.Label(self, text="ETD:")
        self._etd_label.grid(column=0, row=7, sticky=tk.W, padx=10, pady=10)

        self._etd_entry = ttk.Entry(self)
        self._etd_entry.grid(column=1, row=7, sticky=tk.E, padx=10, pady=10)

        self._checkinctr_label = tk.Label(self, text="Check-in Counter:")
        self._checkinctr_label.grid(column=0, row=8, sticky=tk.W, padx=10, pady=10)

        self._checkinctr_entry = ttk.Entry(self)
        self._checkinctr_entry.grid(column=1, row=8, sticky=tk.E, padx=10, pady=10)

        self._status_label = tk.Label(self, text="Status:")
        self._status_label.grid(column=0, row=9, sticky=tk.W, padx=10, pady=10)

        self._status_entry = ttk.Entry(self)
        self._status_entry.grid(column=1, row=9, sticky=tk.E, padx=10, pady=10)

        self._beltstatus_label = tk.Label(self, text="Belt status:")
        self._beltstatus_label.grid(column=0, row=10, sticky=tk.W, padx=10, pady=10)

        self._beltstatus_entry = ttk.Entry(self)
        self._beltstatus_entry.grid(column=1, row=10, sticky=tk.E, padx=10, pady=10)

        self._gate_label = tk.Label(self, text="Gate:")
        self._gate_label.grid(column=0, row=11, sticky=tk.W, padx=10, pady=10)

        self._gate_entry = ttk.Entry(self)
        self._gate_entry.grid(column=1, row=11, sticky=tk.E, padx=10, pady=10)

        self._belt_label = tk.Label(self, text="Belt:")
        self._belt_label.grid(column=0, row=12, sticky=tk.W, padx=10, pady=10)

        self._belt_entry = ttk.Entry(self)
        self._belt_entry.grid(column=1, row=12, sticky=tk.E, padx=10, pady=10)


class EditFlightWindow(FlightWindow):
    def __init__(self, parent, con, id, *args, **kwargs):
        FlightWindow.__init__(self, *args, **kwargs)

        self.__con = con
        self.__id = id
        self._parent = parent

        self.title("Edit Flight")

        self.__edit_button = ttk.Button(self, text="Edit", command=self.__edit)
        self.__edit_button.grid(row=13, column=0, columnspan=2)

        self.__populate()

    def __populate(self):
        cur = self.__con.cursor()
        cur.execute(
            "SELECT `ifid`, `ofid`, `from`, `to`, `sta`, `eta`,"
            " `std`, `etd`, `checkinctr`, `status`, `beltstatus`, "
            "`gate`, `belt` FROM `flight` WHERE id = %(id)s LIMIT 1;",
            {"id": self.__id},
        )
        data = cur.fetchone()
        if data[0]:
            self._ifid_entry.insert(0, data[0])
        if data[1]:
            self._ofid_entry.insert(0, data[1])
        if data[2]:
            self._from_entry.insert(0, data[2])
        if data[3]:
            self._to_entry.insert(0, data[3])
        self._sta_entry.insert(0, data[4])
        self._eta_entry.insert(0, data[5])
        self._std_entry.insert(0, data[6])
        self._etd_entry.insert(0, data[7])
        if data[8]:
            self._checkinctr_entry.insert(0, data[8])
        self._status_entry.insert(0, data[9])
        self._beltstatus_entry.insert(0, data[10])
        if data[11]:
            self._gate_entry.insert(0, data[11])
        if data[12]:
            self._belt_entry.insert(0, data[12])
        ### do ###

        cur.close()

    def __edit(self):
        cur = self.__con.cursor()
        try:
            cur.execute(
                "UPDATE flight SET ifid = %(ifid)s, ofid = %(ofid)s,"
                " `from` = %(from)s, `to`= %(to)s, sta = %(sta)s, "
                "eta = %(eta)s, std = %(std)s, etd = %(etd)s, "
                "checkinctr = %(checkinctr)s, status = %(status)s, "
                "beltstatus = %(beltstatus)s, gate = %(gate)s, "
                "belt = %(belt)s WHERE id =%(id)s;",
                {
                    "id": self.__id,
                    "ifid": self._ifid_entry.get(),
                    "ofid": self._ofid_entry.get(),
                    "from": self._from_entry.get(),
                    "to": self._to_entry.get(),
                    "sta": self._sta_entry.get(),
                    "eta": self._eta_entry.get(),
                    "std": self._std_entry.get(),
                    "etd": self._etd_entry.get(),
                    "checkinctr": self._checkinctr_entry.get(),
                    "status": self._status_entry.get(),
                    "beltstatus": self._beltstatus_entry.get(),
                    "gate": self._gate_entry.get(),
                    "belt": self._belt_entry.get(),
                },
            )
        except OperationalError as e:
            messagebox.showerror(str(type(e)), str(e))
        else:
            self.__con.commit()
            messagebox.showinfo("Success", "Success")
            self._parent._refresh_table()
            self.destroy()
        finally:
            cur.close()


class AddFlightWindow(FlightWindow):
    def __init__(self, parent, con, *args, **kwargs):
        FlightWindow.__init__(self, *args, **kwargs)

        self.__con = con
        self._parent = parent

        self.title("Add Flight")

        self.__add_button = ttk.Button(self, text="Add", command=self.__add)
        self.__add_button.grid(row=13, column=0, columnspan=2)

    def __add(self):
        cur = self.__con.cursor()
        try:
            cur.execute(
                "INSERT INTO FLIGHT (ifid, ofid, `from`, `to`, sta, eta,"
                " std, etd, checkinctr , status, beltstatus, gate, belt) "
                "values (%(ifid)s, %(ofid)s, %(from)s, %(to)s, %(sta)s, "
                "%(eta)s,%(std)s,%(etd)s,%(checkinctr)s,%(status)s, "
                "%(beltstatus)s,%(gate)s,%(belt)s)",
                {
                    "ifid": self._ifid_entry.get(),
                    "ofid": self._ofid_entry.get(),
                    "from": self._from_entry.get(),
                    "to": self._to_entry.get(),
                    "sta": self._sta_entry.get(),
                    "eta": self._eta_entry.get(),
                    "std": self._std_entry.get(),
                    "etd": self._etd_entry.get(),
                    "checkinctr": self._checkinctr_entry.get(),
                    "status": self._status_entry.get(),
                    "beltstatus": self._beltstatus_entry.get(),
                    "gate": self._gate_entry.get(),
                    "belt": self._belt_entry.get(),
                },
            )
        except OperationalError as e:
            messagebox.showerror(str(type(e)), str(e))
        else:
            self.__con.commit()
            messagebox.showinfo("Success", "Success")
            self._parent._refresh_table()
            self.destroy()
        finally:
            cur.close()


"""
"INSERT INTO FLIGHT (ifid, ofid, `from`, `to`, sta, eta,"
" std, etd, checkinctr , status, beltstatus, gate, belt) "
"values (%(ifid)s, %(ofid)s, %(from)s, %(to)s, %(sta)s, "
"%(eta)s,%(std)s,%(etd)s,%(checkinctr)s,%(status)s, "
"%(beltstatus)s,%(gate)s,%(belt)s)"

"""
if __name__ == "__main__":
    root = HomeScreen(login.login())
    root.mainloop()
