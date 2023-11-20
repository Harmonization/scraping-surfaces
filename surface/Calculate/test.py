from .scraping import Table
from .visualize import surface_3d

def main():
    table = Table()
    table.process()
    i = 3
    print(table.surfaces['Точки'][i])
    print(table.surfaces[table.name_1][i])
    surface_3d(table.surfaces['Точки'][i])

if __name__ == '__main__':
    main()