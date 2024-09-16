import customtkinter
import pyarrow.feather as feather
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import pandas as pd
import math

class Plotter(customtkinter.CTkFrame):

    list_of_area_values_cracks = []
    list_of_area_values_gas_pores = []
    list_of_area_values_lack_of_fusion_pores = []

    list_of_roundness_values_cracks = []
    list_of_roundness_values_gas_pores = []
    list_of_roundness_values_lack_of_fusion_pores = []

    list_of_angles_cracks = []
    list_of_angles_gas_pores = []
    list_of_angles_lack_of_fusion_pores = []

    list_of_centeroid_points_cracks = []
    list_of_centeroid_points_gas_pores = []
    list_of_centeroid_points_lack_of_fusion_pores = []

    size=7

    def __init__(self,creator,feather_path):
        super(Plotter, self).__init__(creator)

        df_read = feather.read_feather(feather_path)

        # Iterate over the rows of the DataFrame and print each data cluster
        for index, row in df_read.iterrows():
            # print("\n")

            if row['Pore Identity'] == 'Crack':
                self.list_of_area_values_cracks.append(row['Pore Area'])
                self.list_of_angles_cracks.append(row['Pore Orientation'])
                self.list_of_roundness_values_cracks.append(row['Pore Roundness'])
                self.list_of_centeroid_points_cracks.append(row['Pore Centroid'])

            if row['Pore Identity'] == 'Gas Pore':
                self.list_of_area_values_gas_pores.append(row['Pore Area'])
                self.list_of_angles_gas_pores.append(row['Pore Orientation'])
                self.list_of_roundness_values_gas_pores.append(row['Pore Roundness'])
                self.list_of_centeroid_points_gas_pores.append(row['Pore Centroid'])

            if row['Pore Identity'] == 'Lack of Fusion Pore':
                self.list_of_area_values_lack_of_fusion_pores.append(row['Pore Area'])
                self.list_of_angles_lack_of_fusion_pores.append(row['Pore Orientation'])
                self.list_of_roundness_values_lack_of_fusion_pores.append(row['Pore Roundness'])
                self.list_of_centeroid_points_lack_of_fusion_pores.append(row['Pore Centroid'])


    def bar_chart(self):
        self.clear()
        # Plot 1 - Simple Bar Chart #

        # Calculate the number of each type of defect
        num_cracks = len(self.list_of_area_values_cracks)
        num_gas_pores = len(self.list_of_area_values_gas_pores)
        num_lack_of_fusion_pores = len(self.list_of_area_values_lack_of_fusion_pores)

        # Calculate the average size of each type of defect
        avg_cracks = sum(self.list_of_area_values_cracks) / num_cracks
        avg_gas_pores = sum(self.list_of_area_values_gas_pores) / num_gas_pores
        avg_lack_of_fusion_pores = sum(self.list_of_area_values_lack_of_fusion_pores) / num_lack_of_fusion_pores

        # Data for the chart
        labels = ['Cracks', 'Gas Pores', 'Lack of Fusion Pores']
        counts = [num_cracks, num_gas_pores, num_lack_of_fusion_pores]
        averages = [avg_cracks, avg_gas_pores, avg_lack_of_fusion_pores]
        colors = ['blue', 'green', 'red']

        #-----------------------------------------

        self.frame_1 = Figure(figsize=(self.size, self.size))
        self.can = FigureCanvasTkAgg(self.frame_1, master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.add_subplot()


        #---------------------------------------


        bars = self.axs.bar(labels, counts, color=colors)

        # Add the average size labels on the bars
        for bar, avg in zip(bars, averages):
            yval = bar.get_height()
            self.axs.text(bar.get_x() + bar.get_width() / 2, yval + 0.05 * max(counts), f'Average Size: {avg:.2f}',
                    ha='center', va='top', color='black')

        # Add labels and title
        self.axs.set_ylabel('Number of Defects')
        self.axs.set_title('Number of Each Type of Defect and Their Average Size')


        #--------------------------------------

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()



    def histogram_log_area(self):
        self.clear()


        # Plot 2 - Histogram of log Area Distribution #

        # Convert area values to log base 10
        log_cracks = np.log10(self.list_of_area_values_cracks)
        log_gas_pores = np.log10(self.list_of_area_values_gas_pores)
        log_lack_of_fusion_pores = np.log10(self.list_of_area_values_lack_of_fusion_pores)

        # Calculate histograms
        hist_cracks, bins_cracks = np.histogram(log_cracks, bins='auto')
        hist_gas_pores, bins_gas_pores = np.histogram(log_gas_pores, bins='auto')
        hist_lack_of_fusion_pores, bins_lack_of_fusion_pores = np.histogram(log_lack_of_fusion_pores, bins='auto')

        # Create a list of tuples (histogram, bins, label, color)
        hist_data = [
            (hist_cracks, bins_cracks, 'Cracks', 'blue'),
            (hist_gas_pores, bins_gas_pores, 'Gas Pores', 'green'),
            (hist_lack_of_fusion_pores, bins_lack_of_fusion_pores, 'Lack of Fusion Pores', 'red')
        ]

        # Sort the histograms by the maximum frequency
        hist_data.sort(key=lambda x: max(x[0]), reverse=True)

        #-------------------------------

        self.frame_1 = Figure(figsize=(self.size, self.size))
        self.can = FigureCanvasTkAgg(self.frame_1, master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.add_subplot()

        #--------------------------------


        for hist, bins, label, color in hist_data:
            self.axs.hist(bins[:-1], bins, weights=hist, alpha=0.7, label=label, color=color)

        # Add labels and title
        self.axs.set_xlabel('Log base 10 of Area')
        self.axs.set_ylabel('Frequency')
        self.axs.set_title('Histogram of Log base 10 of Area for Different Defect Types')
        self.axs.legend()

        #-------------------------------

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()

    #TODO:put the 3 plots separated
    def rose_diagram(self):
        self.clear()

        # Plot 3 - Rose Diagrams Side By Side #

        def plot_rose_diagram(ax, data, title, color, bin_edges, agreements=None, annotate=False):
            angles_radians = np.deg2rad(data)
            hist, _ = np.histogram(angles_radians, bins=bin_edges)
            bin_widths = np.diff(bin_edges)
            bars = ax.bar(bin_edges[:-1], hist, width=bin_widths, edgecolor='black', color=color, alpha=0.6)
            ax.set_theta_zero_location('E')
            ax.set_theta_direction(1)
            ax.set_thetalim(0, np.pi)
            ax.set_xticks(np.linspace(0, np.pi, len(bin_edges) // 2 + 1))
            ax.set_xticklabels(
                [f'{int(np.rad2deg(angle))}°' for angle in np.linspace(0, np.pi, len(bin_edges) // 2 + 1)])
            ax.set_title(title)

            if annotate and agreements is not None:
                overall_agreement_5to10, overall_agreement_1to10, bin_agreement_5to10, bin_agreement_1to10 = agreements
                ax.text(0.5, 1.1,
                        f'Agreement 5ys-10ys: {overall_agreement_5to10:.2f}\nAgreement 1ys-10ys: {overall_agreement_1to10:.2f}',
                        transform=ax.transAxes, ha='center', fontsize=10)
                for i, (agreement_5to10, agreement_1to10) in enumerate(zip(bin_agreement_5to10, bin_agreement_1to10)):
                    angle = bin_edges[i] + (bin_edges[i + 1] - bin_edges[i]) / 2
                    ax.text(angle, max(hist) * 0.7, f'{agreement_5to10:.2f}\n{agreement_1to10:.2f}', color='black',
                            ha='center', fontsize=8)

        num_bins = 18
        bin_edges = np.linspace(0, np.pi, num_bins + 1)

        datasets = [self.list_of_angles_cracks, self.list_of_angles_gas_pores, self.list_of_area_values_lack_of_fusion_pores]

        categories = ['Cracks', 'Gas Pores', 'Lack of Fusion Pores']
        colors = ['blue', 'green', 'red']

        # -------------------------------

        self.frame_1 = Figure(figsize=(self.size, self.size))
        self.can = FigureCanvasTkAgg(self.frame_1, master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.subplots(3, 1, subplot_kw={'projection': 'polar'})  # 3 polar subplots

        # --------------------------------

        # Create side-by-side rose diagrams
        for ax, data, title, color in zip(self.axs, datasets, categories, colors):
            plot_rose_diagram(ax, data, title, color, bin_edges)
        self.frame_1.suptitle('Side-by-Side Rose Diagrams')

        self.frame_1.tight_layout()
        # -------------------------------

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()


    def bubble_plot(self):
        self.clear()




        #-----------------------------------------

        # Plot 4 - Bubble Plots #

        area = []
        roundness = []

        area = area + self.list_of_area_values_cracks + self.list_of_area_values_gas_pores + self.list_of_area_values_lack_of_fusion_pores

        roundness = roundness + self.list_of_roundness_values_cracks + self.list_of_roundness_values_gas_pores + self.list_of_roundness_values_lack_of_fusion_pores

        # Create a DataFrame after removing outliers
        df = pd.DataFrame({'Area': area, 'Roundness': roundness})


        # Take the log base 10 of the 'Area' values
        df['LogArea'] = np.log10(0.2 * df['Area'])

        # Define bins - 20 equally distributed bins
        num_bins = 70
        log_area_bins = np.linspace(np.log10(min(df['Area'])), np.log10(max(df['Area'])), num_bins + 1)
        roundness_bins = np.linspace(min(df['Roundness']), max(df['Roundness']), num_bins + 1)

        # Bin the data
        df['LogArea_Bin'] = pd.cut(df['LogArea'], bins=log_area_bins, include_lowest=True, duplicates='drop',
                                   right=False)
        df['Roundness_Bin'] = pd.cut(df['Roundness'], bins=roundness_bins, include_lowest=True, duplicates='drop',
                                     right=False)

        # Categorize data
        def categorize(row):
            if row['Roundness'] < 0.2:
                return 'Cracks'
            elif row['Roundness'] > 0.4:
                return 'Gas Pores'
            return 'Lack of Fusion Pores'

        df['Category'] = df.apply(categorize, axis=1)

        # Compute the frequency
        freq = df.groupby(['LogArea_Bin', 'Roundness_Bin', 'Category'], observed=False).size().reset_index(
            name='Frequency')

        # Create a list to store the frequencies and intervals
        frequency_list = []

        # Loop through the frequency DataFrame to store non-zero frequencies and their intervals
        for index, row in freq.iterrows():
            if row['Frequency'] > 0:
                log_area_mid = (row['LogArea_Bin'].left + row['LogArea_Bin'].right) / 2
                roundness_mid = (row['Roundness_Bin'].left + row['Roundness_Bin'].right) / 2
                frequency = row['Frequency']
                frequency_list.append((log_area_mid, roundness_mid, math.sqrt(frequency)))

        # Print the frequency list with intervals
        # for entry in frequency_list:
        # print(f"LogArea Middle: {entry[0]}, Roundness Middle: {entry[1]}, Frequency: {entry[2]}")

        # Normalize the bubble sizes
        max_freq = freq['Frequency'].max()
        bubble_size_scale = 1000  # Adjust this value to change the max bubble size


        # Define colors for different categories
        category_colors = {
            'Cracks': 'blue',
            'Gas Pores': 'green',
            'Lack of Fusion Pores': 'red'
        }

        #------------------------
        self.frame_1 = Figure(figsize=(self.size, self.size))
        self.can = FigureCanvasTkAgg(self.frame_1, master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.add_subplot()

        #-------------------------


        # Plot bubbles
        legend_handles = []
        for category, color in category_colors.items():
            category_data = freq[freq['Category'] == category]
            handles = self.axs.scatter(
                x=[(bin.left + bin.right) / 2 for bin in category_data['LogArea_Bin']],
                y=[(bin.left + bin.right) / 2 for bin in category_data['Roundness_Bin']],
                # s=(np.sqrt(category_data['Frequency']) / max_freq) * bubble_size_scale,  # normalize bubble size
                s=(category_data['Frequency']) / max_freq * bubble_size_scale,  # normalize bubble size
                c=color,
                alpha=1,
                edgecolors="w",
                linewidth=0.1,
                label=category
            )
            legend_handles.append(handles)

            # Check if category_data is not empty before finding idxmin and idxmax
            if not category_data.empty:
                # Annotate smallest frequency

                min_freq_index = category_data['Frequency'].idxmin()
                min_freq_log_area = (category_data.loc[min_freq_index, 'LogArea_Bin'].left + category_data.loc[
                    min_freq_index, 'LogArea_Bin'].right) / 2
                min_freq_roundness = (category_data.loc[min_freq_index, 'Roundness_Bin'].left + category_data.loc[
                    min_freq_index, 'Roundness_Bin'].right) / 2
                min_freq_value = category_data.loc[min_freq_index, 'Frequency']

                if min_freq_value > 0:
                    self.axs.annotate(min_freq_value, (min_freq_log_area, min_freq_roundness), textcoords="offset points",
                                 xytext=(0, 5),
                                 ha='center')

                # Annotate largest frequency
                max_freq_index = category_data['Frequency'].idxmax()
                max_freq_log_area = (category_data.loc[max_freq_index, 'LogArea_Bin'].left + category_data.loc[
                    max_freq_index, 'LogArea_Bin'].right) / 2
                max_freq_roundness = (category_data.loc[max_freq_index, 'Roundness_Bin'].left + category_data.loc[
                    max_freq_index, 'Roundness_Bin'].right) / 2
                max_freq_value = category_data.loc[max_freq_index, 'Frequency']
                self.axs.annotate(max_freq_value, (max_freq_log_area, max_freq_roundness), textcoords="offset points",
                             xytext=(0, 5),
                             ha='center')

        # Add legend
        self.axs.legend(handles=legend_handles, title='Categories', markerscale=1, scatterpoints=1, loc='upper right')

        # Labels and title
        self.axs.set_xlabel('Log Area (μm)')
        self.axs.set_ylabel('Roundness')
        # plt.title('Bubble Plot of Log Area vs Roundness')
        self.axs.grid(True)


        # -------------------------------

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()



    def distanceVSarea(self):
        self.clear()


        # Convert area values to log base 10
        log_cracks = np.log10(self.list_of_area_values_cracks)
        log_gas_pores = np.log10(self.list_of_area_values_gas_pores)
        log_lack_of_fusion_pores = np.log10(self.list_of_area_values_lack_of_fusion_pores)


        # Plot 5 - Distance From a Point vs Area #

        # Origin point - user defines this by right-clicking a point on the image
        origin = [32, 45]

        # Calculate distances from the origin

        def calculate_distances(coordinates, origin):
            return [np.sqrt((x - origin[0]) ** 2 + (y - origin[1]) ** 2) for x, y in coordinates]

        distances_cracks = calculate_distances(self.list_of_centeroid_points_cracks, origin)
        distances_gas_pores = calculate_distances(self.list_of_centeroid_points_gas_pores, origin)
        distances_lack_of_fusion_pores = calculate_distances(self.list_of_centeroid_points_lack_of_fusion_pores, origin)

        # ------------------------
        self.frame_1 = Figure(figsize=(self.size, self.size))
        self.can = FigureCanvasTkAgg(self.frame_1, master=self)
        self.can.get_tk_widget().pack()
        self.axs = self.frame_1.add_subplot()

        # Plot the data

        self.axs.scatter(distances_cracks, log_cracks, color='blue', alpha=0.6, edgecolors="w", linewidth=0.5, label='Cracks')
        self.axs.scatter(distances_gas_pores, log_gas_pores, color='green', alpha=0.6, edgecolors="w", linewidth=0.5,
                   label='Gas Pores')
        self.axs.scatter(distances_lack_of_fusion_pores, log_lack_of_fusion_pores, color='red', alpha=0.6, edgecolors="w",
                   linewidth=0.5, label='Lack of Fusion Pores')

        self.axs.set_title('Scatter Plot of Area vs Distance from Origin')
        self.axs.set_xlabel('Distance from Origin')
        self.axs.set_ylabel('Log Area')
        self.axs.legend()
        self.axs.grid(True)

        # Adjust layout and show plot
        self.frame_1.tight_layout()

        # -------------------------------

        self.toolbar = NavigationToolbar2Tk(self.can, self)
        self.toolbar.update()
        self.can.get_tk_widget().pack()

        self.can.draw()




    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()