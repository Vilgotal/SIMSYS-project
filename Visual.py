import tkinter as tk
from alphabet import alphabet_upper
import numpy as np
from agent import *
import time


class Visuals:
    def __init__(self, rows: int, columns: int, amount_of_ailes: int, ailes_width: int, corridor_row: int, cell_size=40):

        self.rows = rows+2
        self.columns = columns
        self.amount_of_ailes = amount_of_ailes
        self.ailes_width = ailes_width
        self.cell_size = cell_size
        self.corridor_row = corridor_row
        self.radius = self.cell_size/5

        self.root = tk.Tk()
        self.root.title("Seat Grid")

        self.canvas = tk.Canvas(
            self.root,
            width=self.rows * self.cell_size,                       # rows -> width
            height=(self.columns + self.amount_of_ailes) * self.cell_size,  # columns -> height
            bg="white"
        )
        self.canvas.pack()
        #self.boundaries_list = self.boundaries()
        self.seats = self.seat_indexer()

        self.draw_grid()

        
    def start(self):
        self.root.mainloop()

    def seat_indexer(self):
        """Generates the indexes of the seats 

        Returns:
            seats: list[str]
        """
        seats = []
        for row in range(self.rows):
            for col in range(self.columns):
                seat_id = str(row + 1) + alphabet_upper[col]
                seats.append(seat_id)
        return seats
    

    def aisle_positions(self):
        """Calculating where the positons of the aisles will be located

        Returns:
            index_of_the_aisle: list with len(amount of aisles)
        """
        if self.amount_of_ailes == 1:
            return [self.columns // 2]
        else:
            first = self.columns // 3
            second = 2 * (self.columns // 3) + 1 #Indexing
        
            return [first, second]
        

    def corridor_positions(self):
        if self.corridor_row == 1:
            return {0}
        elif self.corridor_row == 2:
            return {0, self.rows - 1}
        elif self.corridor_row == 3:
            return {0, self.rows // 2, self.rows - 1}
        elif self.corridor_row < 0 or self.corridor_row > 3:
            raise ValueError("corridor_row needst to be between 1-3")
        else:
            return set()
    

    def draw_grid(self):
        if not isinstance(self.rows, int) or not isinstance(self.columns, int):
            raise TypeError("rows & columns needs to be an interger.")
        if self.amount_of_ailes == 0:
            raise ValueError("Must be an aisle in the airplane")
        
        if self.amount_of_ailes > 2:
            raise ValueError(f"An aisle cannot be larger than 2")



        self.aisle_list = self.aisle_positions()
        corridors = self.corridor_positions()

        for i in range(self.rows):
            for j in range(self.columns + self.amount_of_ailes):

                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if i in corridors:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="white", fill="white"
                    )
                    continue

                aisles_before = sum(1 for a in self.aisle_list if a < j)
                if j in self.aisle_list:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="white", fill="white"
                    )
                    continue

                seat_row_idx = i - sum(1 for c in corridors if c < i)
                seat_col = j - aisles_before

                seat_index = seat_row_idx * self.columns + seat_col
                seat_id = self.seats[seat_index]

                # Rita sätet
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")
                
                inner_w = int(self.cell_size * 0.6)
                inner_h = int(self.cell_size * 0.6)
                pad_x = int((self.cell_size - inner_w) // 2)
                pad_y = int((self.cell_size - inner_h) // 2)

                inner_x1 = x1 + pad_x
                inner_y1 = y1 + pad_y

                self.canvas.create_rectangle(
                    inner_x1, inner_y1,
                    inner_x1 + inner_w, inner_y1 + inner_h,
                    outline="black", fill="lightblue"
                )

                self.canvas.create_text(
                    x1 + self.cell_size/2,
                    y1 + self.cell_size/2,
                    text=seat_id,
                    fill="black",
                    font=("Times", 10)
                )
    
    # def boundaries(self):
    #     boundaries = []
    #     for i in range(self.rows):
    #         for j in range(self.columns + self.amount_of_ailes): 
    #             if i == self.corridor_row and i<=self.columns//2 or j in self.aisle_list:
    #                 continue    
    #             else:
    #                 x1 = i * self.cell_size
    #                 y1 = j * self.cell_size
    #                 x2 = x1 + self.cell_size
    #                 y2 = y1 + self.cell_size
    #                 boundaries.append([[x1,y1],[x2,y2]])
    #             return boundaries


    def draw_passenger(self, passenger):
        px = passenger.x * self.cell_size
        py = passenger.y * self.cell_size

        if passenger.seated:
            col = "green"
        elif passenger.luggage_pause > 0 and passenger.luggage_pause < 3:
            col = "red"
        elif passenger.boarding_group == 1:
            col = "#F1C27D"
        elif passenger.boarding_group == 2:
            col = "#E0AC69"
        elif passenger.boarding_group == 3:
            col = "#C68642"
        elif passenger.boarding_group == 4:
            col = "#8D5524"
        elif passenger.boarding_group == 5:
            col = "#FFDBAC"
        else:
            col = "#C68642"
        r = self.radius
        passenger.set_tinker_object(self.canvas.create_oval(
            px + self.cell_size/2 - r,
            py + self.cell_size/2 - r,
            px + self.cell_size/2 + r,
            py + self.cell_size/2 + r,
            fill=col,
            outline="black"
        ))
        passenger.set_tinker_text(self.canvas.create_text(px + self.cell_size/2 ,
            py + self.cell_size/2,
            text=passenger.seat,
            fill="white",
            font=("Times", 10)
            ))

    def update_passenger_position(self, passenger):
        px = passenger.x * self.cell_size
        py = passenger.y * self.cell_size
        r = self.radius

        self.canvas.coords(passenger.tinkerobject, px + self.cell_size/2 - r,
            py + self.cell_size/2 - r,
            px + self.cell_size/2 + r,
            py + self.cell_size/2 + r)
        self.canvas.coords(passenger.tinkertext, px + self.cell_size/2 ,
            py + self.cell_size/2)



    def update_passengers(self, passenger_list):
        if passenger_list is None:
            passenger_list = []


        for p in passenger_list:
            if p.spawned == False:
                self.draw_passenger(p)
                    # sedan passagerare
                #p.spawned = True
            else:
                self.update_passenger_position(p)
                

        return True


