import matplotlib.pyplot as plt
import csv

def plot_temperatures():
    ids = []
    temperatures = []

    with open('dados.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) >= 2:
                try:
                    ids.append(row[0])
                    temperatures.append(int(row[1]))
                except ValueError:
                    # Skip rows with invalid temperature data
                    continue

    # Create a dictionary to store temperatures for each ID
    data_by_id = {}
    for i, temp in zip(ids, temperatures):
        if i not in data_by_id:
            data_by_id[i] = []
        data_by_id[i].append(temp)

    # Plotting
    plt.figure(figsize=(10, 6))
    for sensor_id, temps in data_by_id.items():
        plt.plot(temps, label=f'Sensor {sensor_id}')

    plt.xlabel('Leitura')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperaturas dos Sensores ao Longo do Tempo')
    plt.legend()
    plt.grid(True)
    plt.savefig('temperaturas.png')
    plt.show()

if __name__ == '__main__':
    plot_temperatures()

