import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageTk

# Untuk chart visualisasi trend kendaraan
class ChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="First Chart Page", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button_back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame('HomePage'))
        button_back.pack(fill="x", padx=10, pady=10)

        # Create a button to load and display the chart
        button_chart = ttk.Button(self, text="Show Chart", command=self.show_chart)
        button_chart.pack(fill="x", padx=10, pady=10)

        # Placeholder for the chart
        self.chart_placeholder = ttk.Label(self, text="Chart will be displayed here")
        self.chart_placeholder.pack(pady=20)

    def show_chart(self):
        # Read data from CSV file (replace 'jenis_kendaraan.csv' with the actual file name)
        jenis_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jenistransportasi.csv'
        jumlah_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jumlahtransportasi.csv'

        jenis_data = pd.read_csv(jenis_transportasi_file)
        jumlah_data = pd.read_csv(jumlah_transportasi_file)

        # Merge data based on 'id_jenistransportasi'
        merged_data = pd.merge(jenis_data, jumlah_data, on='id_jenistransportasi')

        # Group by 'jenistransportasi' and sum the 'jumlahtransportasi'
        grouped_data = merged_data.groupby('jenistransportasi')['jumlahtransportasi'].sum()

        # Create a bar chart
        fig, ax = Figure(figsize=(10, 6), dpi=100), None
        try:
            ax = fig.add_subplot(111)
            ax.bar(grouped_data.index, grouped_data.values, color='b', alpha=0.7)
            ax.set_xlabel('Jenis Transportasi')
            ax.set_ylabel('Jumlah Kendaraan')
            ax.set_title('Jumlah Kendaraan Berdasarkan Jenis')
        except Exception as e:
            self.chart_placeholder.config(text="Error creating chart: {}".format(str(e)))
            return

        # Embed the chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

# Untuk chart visualisasi big data pertama
class SecondChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Second Chart Page", font=("Helvetica", 14))
        label.pack(pady=10, padx=10)

        # Back button
        button_back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame('HomePage'))
        button_back.pack(fill="x", padx=10, pady=10)

        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(self)

        # Create tabs
        chart_tab = ttk.Frame(notebook)
        video_tab = ttk.Frame(notebook)

        # Add tabs to the Notebook
        notebook.add(chart_tab, text="Charts")
        notebook.add(video_tab, text="Video")

        # Pack the Notebook widget
        notebook.pack(expand=True, fill="both")

        # Content for the 'Charts' tab
        self.create_chart_tab(chart_tab)

        # Content for the 'Video' tab
        self.create_video_tab(video_tab)

    def create_chart_tab(self, tab):
        # Create a button to load and display the chart
        button_chart = ttk.Button(tab, text="Show Chart", command=self.show_all_charts)
        button_chart.pack(fill="x", padx=10, pady=10)

        # Create a canvas for chart display
        self.chart_canvas = tk.Canvas(tab)
        self.chart_canvas.pack()

    def create_video_tab(self, tab):
        # Create a button to start video
        button_start_video = ttk.Button(tab, text="Start Video", command=self.start_video)
        button_start_video.pack(fill="x", padx=10, pady=10)

        # Placeholder for video canvas
        self.video_canvas = tk.Canvas(tab)
        self.video_canvas.pack()

    def start_video(self):
        # Use a predefined video path
        video_path = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\animation.mp4'

        # Start video playback
        self.play_video(video_path)

    def play_video(self, video_path):
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        width = int(cap.get(3))
        height = int(cap.get(4))

        # Create a canvas for video display
        video_canvas = tk.Canvas(self.video_canvas, width=width, height=height)
        video_canvas.pack()

        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to ImageTk format
            img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))

            # Update the canvas with the new frame
            video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
            video_canvas.update()

            # Pause for a short duration to control the video playback speed
            video_canvas.after(30)

            # Remove the previous frame
            video_canvas.delete("all")

        # Release the video capture object
        cap.release()

    def show_all_charts(self):
        # Create a subplot grid with 2 rows and 2 columns
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

        # Call each chart function with the respective subplot
        self.show_percentage_chart(axs[0, 0])
        self.show_vehicle_counts_chart(axs[0, 1])
        self.show_length_width_relationship_chart(axs[1, 0])
        self.show_average_length_width_chart(axs[1, 1])

        # Adjust layout
        plt.tight_layout()

        # Embed the chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_second_chart(self):
        # Call the function to show all charts
        self.show_all_charts()

    def show_percentage_chart(self, ax):
        # Read data from CSV files
        jenis_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jenistransportasi.csv'
        jumlah_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jumlahtransportasi.csv'

        jenis_data = pd.read_csv(jenis_transportasi_file)
        jumlah_data = pd.read_csv(jumlah_transportasi_file)

        # Merge data based on 'id_jenistransportasi'
        merged_data = pd.merge(jenis_data, jumlah_data, on='id_jenistransportasi')

        # Group by 'jenistransportasi' and calculate the sum of 'jumlahtransportasi'
        grouped_data = merged_data.groupby('jenistransportasi')['jumlahtransportasi'].sum().reset_index()

        # Calculate the percentage
        total_count = grouped_data['jumlahtransportasi'].sum()
        grouped_data['percentage'] = (grouped_data['jumlahtransportasi'] / total_count) * 100

        # Create a pie chart for percentage
        try:
            ax.pie(grouped_data['percentage'], labels=grouped_data['jenistransportasi'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Persentase Jenis Kendaraan')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))

    def show_vehicle_counts_chart(self, ax):
        # Read data from CSV files
        jenis_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jenistransportasi.csv'
        jumlah_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jumlahtransportasi.csv'

        jenis_data = pd.read_csv(jenis_transportasi_file)
        jumlah_data = pd.read_csv(jumlah_transportasi_file)

        # Merge data based on 'id_jenistransportasi'
        merged_data = pd.merge(jenis_data, jumlah_data, on='id_jenistransportasi')

        # Group by 'jenistransportasi' and sum the 'jumlahtransportasi'
        grouped_data = merged_data.groupby('jenistransportasi')['jumlahtransportasi'].sum()

        # Create a bar chart for vehicle counts
        try:
            ax.bar(grouped_data.index, grouped_data.values, color='b', alpha=0.7)
            #ax.set_xlabel('Jenis Transportasi')
            ax.set_ylabel('Jumlah Kendaraan')
            ax.set_title('Perbandingan Jumlah Jenis Kendaraan')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

    def show_length_width_relationship_chart(self, ax):
        # Read data from CSV files
        jenis_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jenistransportasi.csv'

        jenis_data = pd.read_csv(jenis_transportasi_file)

        # Group by 'your_group_column'
        grouped_data = jenis_data.groupby('jenistransportasi')

        # Create a scatter plot for length and width relationship for each group
        try:
            for name, group in grouped_data:
                ax.scatter(group['panjang_jenistransportasi'], group['lebar_jenistransportasi'], label=name, alpha=0.7)

            ax.set_xlabel('Panjang Kendaraan')
            ax.set_ylabel('Lebar Kendaraan')
            ax.set_title('Hubungan antara Panjang dan Lebar Kendaraan')
            ax.legend(title='Group')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

    def show_average_length_width_chart(self, ax):
        # Read data from CSV files
        jenis_transportasi_file = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\jenistransportasi.csv'

        jenis_data = pd.read_csv(jenis_transportasi_file)

        # Group by 'jenistransportasi'
        grouped_data = jenis_data.groupby('jenistransportasi')

        # Calculate average length and width for each group
        avg_lengths = grouped_data['panjang_jenistransportasi'].mean()
        avg_widths = grouped_data['lebar_jenistransportasi'].mean()

        # Create positions for bars
        positions = np.arange(len(avg_lengths))

        # Set height for the bars
        bar_height = 0.35

        # Create a bar chart for average length and width for each group
        try:
            ax.barh(positions, avg_lengths, height=bar_height, color='b', alpha=0.7, label='Average Length')
            ax.barh(positions + bar_height, avg_widths, height=bar_height, color='g', alpha=0.7, label='Average Width')

            # Set labels and title
            ax.set_yticks(positions + bar_height / 2)
            ax.set_yticklabels(avg_lengths.index)
            ax.set_ylabel('Jenis Transportasi')
            ax.set_xlabel('Average Value')
            ax.set_title('Rata-rata Panjang dan Lebar Kendaraan')
            ax.legend(title='Metric', loc='lower right')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

# Untuk chart visualisasi big data kedua
class ThirdChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Third Chart Page", font=("Helvetica", 14))
        label.pack(pady=10, padx=10)

        # Back button
        button_back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame('HomePage'))
        button_back.pack(fill="x", padx=10, pady=10)

        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(self)

        # Create tabs
        chart_tab = ttk.Frame(notebook)
        video_tab = ttk.Frame(notebook)

        # Add tabs to the Notebook
        notebook.add(chart_tab, text="Charts")
        notebook.add(video_tab, text="Video")

        # Pack the Notebook widget
        notebook.pack(expand=True, fill="both")

        # Content for the 'Charts' tab
        self.create_chart_tab(chart_tab)

        # Content for the 'Video' tab
        self.create_video_tab(video_tab)

    def create_chart_tab(self, tab):
        # Create a button to load and display the chart
        button_chart = ttk.Button(tab, text="Show Chart", command=self.show_all_charts)
        button_chart.pack(fill="x", padx=10, pady=10)

        # Create a canvas for chart display
        self.chart_canvas = tk.Canvas(tab)
        self.chart_canvas.pack()

    def create_video_tab(self, tab):
        # Create a button to start video
        button_start_video = ttk.Button(tab, text="Start Video", command=self.start_video)
        button_start_video.pack(fill="x", padx=10, pady=10)

        # Placeholder for video canvas
        self.video_canvas = tk.Canvas(tab)
        self.video_canvas.pack()

    def start_video(self):
        # Use a predefined video path
        video_path = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\animation.mp4' # ganti sesuai kebutuhan

        # Start video playback
        self.play_video(video_path)

    def play_video(self, video_path):
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        width = int(cap.get(3))
        height = int(cap.get(4))

        # Create a canvas for video display
        video_canvas = tk.Canvas(self.video_canvas, width=width, height=height)
        video_canvas.pack()

        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to ImageTk format
            img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))

            # Update the canvas with the new frame
            video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
            video_canvas.update()

            # Pause for a short duration to control the video playback speed
            video_canvas.after(30)

            # Remove the previous frame
            video_canvas.delete("all")

        # Release the video capture object
        cap.release()

    def show_all_charts(self):
        # Create a subplot grid with 2 rows and 2 columns
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

        # Call each chart function with the respective subplot
        self.show_percentage_chart(axs[0, 0])
        self.show_bar_chart(axs[0, 1])
        self.show_engine_fuel_relationship_chart(axs[1, 0])
        self.show_average_engine_fuel_chart(axs[1, 1])

        # Adjust layout
        plt.tight_layout()

        # Embed the chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_second_chart(self):
        # Call the function to show all charts
        self.show_all_charts()

    def show_percentage_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\CARS_1.csv'
        used_car = pd.read_csv(car_data)

        # Calculate the percentage
        total_count = used_car['fuel_type'].value_counts(normalize=True) * 100

        # Create a pie chart for percentage
        try:
            ax.pie(total_count, labels=total_count.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#c992f0'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Persentase Tipe Bahan Bakar Mobil')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))

    def show_bar_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\CARS_1.csv'
        used_car = pd.read_csv(car_data)
        total_count = used_car['fuel_type'].value_counts(normalize=True)

        # Create a bar chart for vehicle counts
        try:
            ax.bar(total_count.index, total_count.values, color='b', alpha=0.7)
            #ax.set_xlabel('Jenis Transportasi')
            ax.set_ylabel('Bahan Bakar')
            ax.set_title('Perbandingan Bahan Bakar Mobil')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

    def show_engine_fuel_relationship_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\CARS_1.csv'
        used_car = pd.read_csv(car_data)
        unique_fuel = used_car['fuel_type'].unique()

        try:
            for fuel in unique_fuel:
                fuel_data = used_car[used_car['fuel_type'] == fuel]
                ax.scatter(fuel_data['engine_displacement'], fuel_data['fuel_tank_capacity'], label=fuel, alpha=0.7)

            ax.set_xlabel('Engine Displacement')
            ax.set_ylabel('Fuel Tank Capacity')
            ax.set_title('Hubungan Antara Engine Displacement dan Fuel Tank Capacity')
            ax.legend(title='Fuel')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

    def show_average_engine_fuel_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\CARS_1.csv'
        used_car = pd.read_csv(car_data)

        grouped_data = used_car.groupby('fuel_type')

        # Calculate average 
        avg_mil= grouped_data['engine_displacement'].mean()
        avg_price = grouped_data['fuel_tank_capacity'].mean()

        # Create positions for bars
        positions = np.arange(len(avg_mil))

        # Set height for the bars
        bar_height = 0.35
        try:
            ax.barh(positions, avg_mil, height=bar_height, color='b', alpha=0.7, label='Average ED')
            ax.barh(positions + bar_height, avg_price, height=bar_height, color='g', alpha=0.7, label='FTC')

            # Set labels and title
            ax.set_yticks(positions + bar_height / 2)
            ax.set_yticklabels(avg_mil.index)
            ax.set_ylabel('Engine Displacement')
            ax.set_xlabel('Fuel Tank Capacity')
            ax.set_title('Rata-rata Engine Displacement dan Fuel Tank Capacity')
            ax.legend(title='Metric', loc='lower right')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

# Untuk chart visualisasi big data ketiga
class FourthChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Fourth Chart Page", font=("Helvetica", 14))
        label.pack(pady=10, padx=10)

        # Back button
        button_back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame('HomePage'))
        button_back.pack(fill="x", padx=10, pady=10)

        # Create a Notebook (tabbed interface)
        notebook = ttk.Notebook(self)

        # Create tabs
        chart_tab = ttk.Frame(notebook)
        video_tab = ttk.Frame(notebook)

        # Add tabs to the Notebook
        notebook.add(chart_tab, text="Charts")
        notebook.add(video_tab, text="Video")

        # Pack the Notebook widget
        notebook.pack(expand=True, fill="both")

        # Content for the 'Charts' tab
        self.create_chart_tab(chart_tab)

        # Content for the 'Video' tab
        self.create_video_tab(video_tab)

    def create_chart_tab(self, tab):
        # Create a button to load and display the chart
        button_chart = ttk.Button(tab, text="Show Chart", command=self.show_all_charts)
        button_chart.pack(fill="x", padx=10, pady=10)

        # Create a canvas for chart display
        self.chart_canvas = tk.Canvas(tab)
        self.chart_canvas.pack()

    def create_video_tab(self, tab):
        # Create a button to start video
        button_start_video = ttk.Button(tab, text="Start Video", command=self.start_video)
        button_start_video.pack(fill="x", padx=10, pady=10)

        # Placeholder for video canvas
        self.video_canvas = tk.Canvas(tab)
        self.video_canvas.pack()

    def start_video(self):
        # Use a predefined video path
        video_path = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\animation.mp4'

        # Start video playback
        self.play_video(video_path)

    def play_video(self, video_path):
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        width = int(cap.get(3))
        height = int(cap.get(4))

        # Create a canvas for video display
        video_canvas = tk.Canvas(self.video_canvas, width=width, height=height)
        video_canvas.pack()

        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to ImageTk format
            img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))

            # Update the canvas with the new frame
            video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
            video_canvas.update()

            # Pause for a short duration to control the video playback speed
            video_canvas.after(30)

            # Remove the previous frame
            video_canvas.delete("all")

        # Release the video capture object
        cap.release()

    def show_all_charts(self):
        # Create a subplot grid with 2 rows and 2 columns
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

        # Call each chart function with the respective subplot
        self.show_percentage_chart(axs[0, 0])
        self.show_type_counts_chart(axs[0, 1])
        self.show_length_width_relationship_chart(axs[1, 0])
        self.show_average_length_width_chart(axs[1, 1])

        # Adjust layout
        plt.tight_layout()

        # Embed the chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_second_chart(self):
        # Call the function to show all charts
        self.show_all_charts()

    def show_percentage_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\Cars_India_dataset.csv'
        used_car = pd.read_csv(car_data)

        # Calculate the percentage
        total_count = used_car['Type'].value_counts(normalize=True) * 100

        # Create a pie chart for percentage
        try:
            ax.pie(total_count, labels=total_count.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#c992f0'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Persentase Brand Mobil')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))

    def show_type_counts_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\Cars_India_dataset.csv'
        used_car = pd.read_csv(car_data)
        total_count = used_car['Type'].value_counts(normalize=True)

        # Create a bar chart for vehicle counts
        try:
            ax.bar(total_count.index, total_count.values, color='b', alpha=0.7)
            #ax.set_xlabel('Jenis Transportasi')
            ax.set_ylabel('Jumlah Tipe Mobil')
            ax.set_title('Perbandingan Jumlah Tipe Mobil')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

    def show_length_width_relationship_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\Cars_India_dataset.csv'
        used_car = pd.read_csv(car_data)

        unique_brands = used_car['Type'].unique()

        # Create a scatter plot for mileage and price for each brand
        try:
            for brand in unique_brands:
                brand_data = used_car[used_car['Type'] == brand]
                ax.scatter(brand_data['Length'], brand_data['Width'], label=brand, alpha=0.7)

            ax.set_xlabel('Length')
            ax.set_ylabel('Width')
            ax.set_title('Hubungan Antara Panjang dan Lebar Tiap Tipe')
            ax.legend(title='Type')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return


    def show_average_length_width_chart(self, ax):
        # Read data from CSV files
        car_data = r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\Cars_India_dataset.csv'
        used_car = pd.read_csv(car_data)

        grouped_data = used_car.groupby('Type')

        # Calculate average length and width for each group
        avg_len = grouped_data['Length'].mean()
        avg_wid = grouped_data['Width'].mean()

        # Create positions for bars
        positions = np.arange(len(avg_len))

        # Set height for the bars
        bar_height = 0.35
        try:
            ax.barh(positions, avg_len, height=bar_height, color='b', alpha=0.7, label='Average Length')
            ax.barh(positions + bar_height, avg_wid, height=bar_height, color='g', alpha=0.7, label='Average Width')

            # Set labels and title
            ax.set_yticks(positions + bar_height / 2)
            ax.set_yticklabels(avg_len.index)
            ax.set_ylabel('Tipe Mobil')
            ax.set_xlabel('Average Value')
            ax.set_title('Rata-rata Panjang dan Lebar')
            ax.legend(title='Metric', loc='lower right')
        except Exception as e:
            print("Error creating chart: {}".format(str(e)))
            return

# Untuk tampilan halaman utama
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Halaman Utama", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 16))  # Ganti ukuran font sesuai kebutuhan

        # first button
        button_first_chart_page = ttk.Button(self, text="Visualisasi Trend Kendaraan", command=lambda: controller.show_frame('ChartPage'))
        button_first_chart_page.pack(fill="x", padx=10, pady=10)

        # second button
        button_second_chart_page = ttk.Button(self, text="Visualisasi Big Data 1", command=lambda: controller.show_frame('SecondChartPage'))
        button_second_chart_page.pack(fill="x", padx=10, pady=10)

        # third button
        button_third_chart_page = ttk.Button(self, text="Visualisasi Big Data 2", command=lambda: controller.show_frame('ThirdChartPage'))
        button_third_chart_page.pack(fill="x", padx=10, pady=10)

        # fourth button
        button_fourth_chart_page = ttk.Button(self, text="Visualisasi Big Data 3", command=lambda: controller.show_frame('FourthChartPage'))
        button_fourth_chart_page.pack(fill="x", padx=10, pady=10)

        # Button to show videos on the home page
        button_vid = ttk.Button(self, text="Show Videos", command=self.show_videos_on_homepage)
        button_vid.pack(fill="x", padx=10, pady=10)

        # Create a frame to hold video canvases
        self.video_frame = tk.Frame(self)
        self.video_frame.pack(side="top", fill="both", expand=True)

        # Canvas for video display
        self.video_canvases = []

    def show_videos_on_homepage(self):
        # Use predefined video paths, bisa diganti sesuai keinginan
        video_paths = [r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\music.mp4', r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\music.mp4', r'C:\Users\ARYA_ADI_P\OneDrive\Documents\Arya Adi\Bigdata\GUI TKINTER\music.mp4']

        # Create a Canvas for each video and embed it in the video_frame
        for video_path in video_paths:
            video_canvas = tk.Canvas(self.video_frame, width=320, height=240)
            video_canvas.pack(side="left", padx=10)
            self.video_canvases.append(video_canvas)

            # Start video playback
            self.controller.play_video(video_path, video_canvas)
        
# Main application
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set window title
        self.title("Chart Visualization")

        # Create container to hold different frames/pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, ChartPage, SecondChartPage, ThirdChartPage, FourthChartPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page by default
        self.show_frame('HomePage')  

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def play_video(self, video_path, canvas):
        # Video playback logic using cv2.VideoCapture
        cap = cv2.VideoCapture(video_path)

        def update_frame():
            nonlocal self
            ret, frame = cap.read()
            if ret:
                # Convert the frame to RGB format
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to ImageTk format
                image = Image.fromarray(rgb_frame)
                self.imgtk = ImageTk.PhotoImage(image=image)

                # Update the canvas with the new frame
                canvas.imgtk = self.imgtk
                canvas.create_image(0, 0, anchor='nw', image=self.imgtk)

                # Schedule the next update
                canvas.after(30, update_frame)
            else:
                # Video has ended, release the capture
                cap.release()


        # Start the first update
        update_frame()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = SampleApp()
    app.geometry("800x600")
    app.mainloop()