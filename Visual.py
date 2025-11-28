import tkinter as tk
from alphabet import alphabet_upper


#Göra en lista med radupplägg istället, [3,3] blir 3-korridor-3 säten och antal korridorer len -1

class Visuals:
    def __init__(self, rows: int, columns: int, amount_of_ailes: int, ailes_width: int, cell_size=40): 
        self.rows = rows
        self.columns = columns
        self.amount_of_ailes = amount_of_ailes
        self.ailes_width = ailes_width
        self.cell_size = cell_size

        self.root = tk.Tk()
        self.root.title("Seat Grid")

        self.canvas = tk.Canvas(
            self.root,
            width=self.rows * self.cell_size,                       # rows -> width
            height=(self.columns + self.amount_of_ailes) * self.cell_size,  # columns -> height
            bg="white"
        )
        self.canvas.pack()

        # Generera sätelista endast en gång
        self.seats = self.seat_indexer()

        # Rita rutnät
        self.draw_grid()

        self.root.mainloop()

        if columns//2 != 0:
            raise ValueError("Columns must be an even value ")

    def seat_indexer(self):
        seats = []
        for row in range(self.rows):
            for col in range(self.columns):
                # Exempel: rad 0 = 1A, rad 1 = 2A
                seat_id = str(row + 1) + alphabet_upper[col]
                seats.append(seat_id)
        return seats
    
    def draw_grid(self):
        if self.amount_of_ailes == 0:
            raise ValueError("Must be an Aisle in the airplane")
        if self.amount_of_ailes == 1:
            aisle_col = self.columns // 2  


        for i in range(self.rows):         # X-led (framåt i planet)
            for j in range(self.columns + self.amount_of_ailes):  # Y-led (vänster ↔ höger i planet)

                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if j == aisle_col:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="black", fill="white"
                    )
                    continue

                seat_col = j if j < aisle_col else j - 1
                seat_index = i * self.columns + seat_col
                seat_id = self.seats[seat_index]

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                self.canvas.create_text(
                    x1 + self.cell_size/2,
                    y1 + self.cell_size/2,
                    text=seat_id,
                    fill="black",
                    font=("Times", 10)
                )


# Kör visualisering
visual_system = Visuals(rows=30, columns=6, amount_of_ailes=1, ailes_width=2)
