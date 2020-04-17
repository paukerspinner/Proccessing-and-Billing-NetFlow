import tkinter as tk
from traffic import *
import datetime
import matplotlib.pyplot as plt

IP = '77.74.181.52'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.traffic = Traffic(IP)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.labelIp = tk.Label(self, text='IP аддрес')
        self.labelIp.grid(row=1, column=1, padx=8, pady=8)

        self.txtIp = tk.Text(self, height=1, width=18)
        self.txtIp.insert('1.0', IP)
        self.txtIp.grid(row=1, column=2, padx=8, pady=8)

        self.btCalTarriff = tk.Button(self, text='Тарификация', command=self.showCalculation)
        self.btCalTarriff.grid(row=2, column=1, columnspan=2, padx=8, pady=8)

        self.labelTraffic = tk.Label(self, text='Трафик (Кб)')
        self.labelTraffic.grid(row=3, column=1, padx=8, pady=8)

        self.txtTraffic = tk.Text(self, height=1, width=18)
        self.txtTraffic.grid(row=3, column=2, padx=8, pady=8)

        self.labelTotalCost = tk.Label(self, text='Итоговая стоимость (Руб)')
        self.labelTotalCost.grid(row=4, column=1, padx=8, pady=8)

        self.txtTotalCost = tk.Text(self, height=1, width=18)
        self.txtTotalCost.grid(row=4, column=2, padx=8, pady=8)

        self.btShowGraphic = tk.Button(self, text='Построить график', command=self.showGraphic)
        self.btShowGraphic.grid(row=8, column=1, columnspan=2, padx=8, pady=8)

    def showCalculation(self):
        self.txtTotalCost.delete('1.0', 'end-1c')
        self.txtTraffic.delete('1.0', 'end-1c')
        self.txtTraffic.insert('1.0', str(self.traffic.calculateTraffic()))
        self.txtTotalCost.insert('1.0', str(self.traffic.calculateTarrif()))

    def showGraphic(self):
        data = self.traffic.trafficByTime()
        timeArr = sorted(data.keys())
        timeArr0 = [datetime.datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in timeArr]
        totalTrafficArr = [data.get(timeArr[0])]
        for i in range(1, len(timeArr)):
            totalTrafficArr.append(totalTrafficArr[i-1] + data.get(timeArr[i]))
        plt.plot(timeArr0, totalTrafficArr)
        plt.xticks(rotation=30)
        plt.ylabel("Объема трафика (Кб)")
        plt.xlabel('Времени')
        plt.title('График зависимости объема трафика от времени')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("Обработка и тарификация трафика NetFlow")
    app.mainloop()