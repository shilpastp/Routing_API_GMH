import csv
import json
import os
import requests
import time
import tkinter

import sys

import config
from tkinter import filedialog as tkfiledialog
from tkinter import messagebox

current_file_path = ""
input_file_path = ""
output_file_path = ""
API_path = config.API_path


class Form1(tkinter.Frame):
    global input_file_path
    global output_file_path

    def __init__(self, root):
        """
        Constructor override function
        TKinter UI code
        :param root: TKinter object
        """
        tkinter.Frame.__init__(self, root)

        self.Label_Input = tkinter.Label(self, text='Select input directory:').grid(row=0, column=0, sticky='e')
        self.Label_Output = tkinter.Label(self, text='Select output directory:').grid(row=1, column=0, sticky='e')
        self.Label_hrs = tkinter.Label(self, text='Starting Delay (hours):').grid(row=4, column=0, sticky='e')
        self.Label_interval = tkinter.Label(self, text='Interval (minutes):').grid(row=6, column=0, sticky='e')
        self.Label_duration = tkinter.Label(self, text='Duration (hours):').grid(row=7, column=0, sticky='e')

        self.text_box_Input = tkinter.Entry(self)
        self.text_box_Input.config(state="disabled")
        self.text_box_Input.grid(row=0, column=1)

        self.text_box_Output = tkinter.Entry(self)
        self.text_box_Output.config(state="disabled")
        self.text_box_Output.grid(row=1, column=1)

        self.text_box_hrs = tkinter.Entry(self)
        self.text_box_hrs.config(state="normal")
        self.text_box_hrs.grid(row=4, column=1, columnspan=1, sticky='w')

        self.text_box_interval = tkinter.Entry(self)
        self.text_box_interval.config(state="normal")
        self.text_box_interval.grid(row=6, column=1, columnspan=2, sticky='w')

        self.text_box_duration = tkinter.Entry(self)
        self.text_box_duration.config(state="normal")
        self.text_box_duration.grid(row=7, column=1, columnspan=2, sticky='w')

        tkinter.Button(self, text='...', command=self.askOpenInput_Dir).grid(row=0, column=2)
        tkinter.Button(self, text='...', command=self.askOpenOutput_Dir).grid(row=1, column=2)
        tkinter.Button(self, text='OK', command=self.get_GeoCode_CSV).grid(row=8, columnspan=2, rowspan=3)

        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Select input Directory'

        self.dir_opt_1 = options_1 = {}
        options_1['initialdir'] = 'C:\\'
        options_1['mustexist'] = False
        options_1['parent'] = root
        options_1['title'] = 'Select output Directory'

    def askOpenInput_Dir(self):
        """
        Input: self
        Process: get input path from the GUI and check for the length of the path
        :return: input path from GUI
        """

        input_path_tkinter = tkfiledialog.askdirectory(**self.dir_opt)
        if len(input_path_tkinter) > 0:
            self.text_box_Input.config(state="normal")
        else:
            self.text_box_Input.config(state="disabled")
        self.text_box_Input.delete(0, 500)
        self.text_box_Input.insert(0, input_path_tkinter)
        return input_path_tkinter

    def askOpenOutput_Dir(self):
        """
        Input: self
        Process: get output path from the GUI and check for the length of the path
        :return: output path from GUI
        """
        output_path_tkinter = tkfiledialog.askdirectory(**self.dir_opt_1)
        if len(output_path_tkinter) > 0:
            self.text_box_Output.config(state="normal")
        else:
            self.text_box_Output.config(state="disabled")
        self.text_box_Output.delete(0, 500)
        self.text_box_Output.insert(0, output_path_tkinter)
        return output_path_tkinter

    def get_GeoCode_CSV(self):
        """
        Input: self
        Process:
        :return:
        """
        print("[" + str(time.ctime()) + "]        " + """
        Following APIs are being used currently:

        1): {0},
        2): {1},
        3): {2}

        """.format(API_path["Here"], API_path["Google"], API_path["MMI"]))
        global input_file_path
        global output_file_path
        input_file_path = self.text_box_Input.get()
        output_file_path = self.text_box_Output.get()
        # log_path = output_file_path
        # log_file = open(log_path + '/log_' + str(time.time()) + '.log', 'w')
        # sys.stdout = log_file
        # sys.stderr = log_file
        start_time = time.time()
        print("[" + str(time.ctime()) + "]        " + 'Process started')
        try:
            input_hrs = abs(int(self.text_box_hrs.get()))
            interval = abs(int(self.text_box_interval.get()))
            end_duration = abs(int(self.text_box_duration.get()))
        except Exception:
            messagebox.showerror("Info", "Time should be in positive integers")
            return ()
        print("[" + str(time.ctime()) + "]        " + "Input Directory:" + input_file_path)
        print("[" + str(time.ctime()) + "]        " + "Output Directory:" + output_file_path)
        if len(input_file_path) == 0:
            print("[" + str(time.ctime()) + "]        " + "Enter the input file path")
            messagebox.showerror("Info", "Enter the input file path")
            return ()
        elif len(output_file_path) == 0:
            print("[" + str(time.ctime()) + "]        " + "Enter the output file path")
            messagebox.showerror("Info", "Enter the output file path")
            return ()
        time.sleep(input_hrs * 3600)
        directory_path_in = input_file_path
        directory_output_path = output_file_path
        counter = 0
        while True:
            itr_start_time = time.time()
            print("[" + str(time.ctime()) + "]        " + 'Currently on Iteration Number {0}'.format(counter))
            counter += 1
            for file in os.listdir(directory_path_in):
                if file.endswith(".csv"):
                    with open(directory_path_in + "/" + file, 'r') as csvfile:
                        with open(directory_output_path + "/Traffic_Benchmarking_" + str(
                                int(time.time())) + ".csv", 'a') as csvfile_write:
                            writecsv = csv.writer(csvfile_write, delimiter=',', lineterminator='\n')
                            readCSV = csv.DictReader(csvfile)
                            writecsv.writerow(["UID", "Start Point", "End Point", "Path for MMI API",
                                               "MMI Date", "MMI Time", "MMI length_meter", "MMI eta_sec",
                                               "Google Distance", "Google Duration", "Here Distance",
                                               "Here trafficTime"])
                            for row in readCSV:
                                UID = int(row["S. No."])
                                start = row["Start Point"]
                                end = row["End Point"]
                                mmi_path = row["Path for MMI API"]
                                start_here = 'waypoint0=geo!' + str(row["Start Point"])
                                end_here = 'waypoint1=geo!' + (row["End Point"])
                                start_google = 'origin=' + str(row["Start Point"])
                                end_google = 'destination=' + (row["End Point"])
                                if len(start) and len(end) > 0:
                                    here_url = (API_path["Here"].replace('waypoint0=geo!', start_here)).replace(
                                        'waypoint1=geo!', end_here)
                                    google_url = (API_path["Google"].replace('origin=', start_google)).replace(
                                        'destination=', end_google)
                                    payload = {'path': mmi_path, 'buffer': '1'}
                                    try:
                                        here_response = requests.get(here_url)
                                        google_response = requests.get(google_url)
                                        mmi_response = requests.post(API_path["MMI"], headers=payload)
                                    except Exception as e:
                                        print("[" + str(time.ctime()) + "]" +
                                              "Server request out of time--- Server may be down/ check your internet "
                                              "connection")
                                        continue
                                    try:
                                        here_data = json.loads(here_response.text)
                                        google_data = json.loads(google_response.text)
                                        mmi_data = json.loads(mmi_response.text)
                                    except:
                                        print("["+str(time.ctime())+"]"+"skipping inputs due to null response")
                                        continue
                                    try:
                                        if here_data and google_data and mmi_data:
                                            here_first_response_data = here_data["response"]['route'][0]['summary']
                                            google_first_response_data = google_data["routes"]
                                            mmi_first_response_data = mmi_data["eta"]
                                            mmi_creation_time = mmi_data["creationTime"].split('T')
                                            mmi_dte = mmi_creation_time[0]
                                            mmi_tym = mmi_creation_time[1][:-1]
                                            writecsv.writerow([UID, start, end, mmi_path, mmi_dte, mmi_tym,
                                                               mmi_first_response_data[0]["length_meter"],
                                                               mmi_first_response_data[0]["eta_sec"],
                                                               google_first_response_data[0]['legs'][0]["distance"][
                                                                   "value"],
                                                               google_first_response_data[0]['legs'][0]["duration"][
                                                                   "value"],
                                                               here_first_response_data["distance"],
                                                               here_first_response_data["trafficTime"]])
                                        else:
                                            writecsv.writerow(
                                                [UID, start, end, mmi_path, "", "", "", "", "", "", "", ""])
                                    except Exception as e:
                                        print("["+str(time.ctime())+"]"+"Error: {0}".format(e))
                                        # if here_data:
                                        #     print(here_data, '\n')
                                        # if mmi_data:
                                        #     print(mmi_data, '\n')
                                        # if google_data:
                                        #     print(google_data)
                                        if str(e) in "list index out of range":
                                            messagebox.showinfo("Info", "Google usage limit exceeded !")
                                            # sys.stdout.close()
                                            # sys.stderr.close()
                                            return ()
                                        continue
                    csvfile.close()
                    csvfile_write.close()
                iteration_time = time.time() - itr_start_time
                if (interval * 60) < iteration_time:
                    continue
                else:
                    print(
                        "[{0}]{1}".format(str(time.ctime()), 'Waiting for next Iteration number: {0}'.format(counter)))
                    time.sleep((interval * 60) - iteration_time)
            if time.time() - itr_start_time >= (end_duration * 3600):
                break
            del itr_start_time
        time_taken = time.time() - start_time
        print("["+str(time.ctime())+"]"+'Task Completed in {0} minutes'.format(time_taken / 60))
        messagebox.showinfo("Info", "Task completed")
        # sys.stdout.close()
        # sys.stderr.close()


if __name__ == '__main__':
    root_0 = tkinter.Tk()
    Form1(root_0).pack()
    root_0.mainloop()
