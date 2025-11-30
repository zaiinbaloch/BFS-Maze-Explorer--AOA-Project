import tkinter as tk
from tkinter import messagebox
import time
from collections import deque

class BFSMazeExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Maze Explorer")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1a2a6c')
        
        # Game variables
        self.maze_size = 15
        self.cell_size = 35
        self.maze = []
        self.current_position = (1, 1)
        self.start_position = (1, 1)
        self.end_position = (13, 13)
        self.steps = 0
        self.undone_steps = 0
        self.move_history = []
        self.game_completed = False
        
        # BFS variables
        self.bfs_visited = set()
        self.bfs_queue = deque()
        self.bfs_parent = {}
        self.bfs_running = False
        self.shortest_path = []
        
        # Path lengths will be calculated by BFS
        self.paths = {
            "best": 0,   # Will be set after BFS
            "avg": 0,    # Will be calculated
            "worst": 0   # Will be calculated
        }
        
        # Colors
        self.colors = {
            'wall': '#2c3e50',
            'path': '#3498db',
            'start': '#2ecc71',
            'end': '#e74c3c',
            'current': '#f1c40f',
            'visited': '#9b59b6',
            'shortest': '#1abc9c',
            'text': 'white',
            'bg_dark': '#1a2a6c',
            'bg_light': '#2c3e50',
            'panel_bg': '#34495e'
        }
        
        self.setup_ui()
        self.initialize_maze()
        self.calculate_path_lengths()
        self.draw_maze()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="BFS Maze Explorer", 
                              font=('Arial', 24, 'bold'), fg='white', bg=self.colors['bg_dark'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Navigate through the maze using BFS concepts. Find the shortest path from start to finish.",
                                 font=('Arial', 12), fg='white', bg=self.colors['bg_dark'], wraplength=800)
        subtitle_label.pack(pady=5)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        content_frame.pack(fill='both', expand=True, padx=20)
        
        # Left frame for maze
        left_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Maze canvas
        self.canvas = tk.Canvas(left_frame, width=self.maze_size * self.cell_size + 10, 
                               height=self.maze_size * self.cell_size + 10, 
                               bg='#2c3e50', highlightthickness=2, highlightbackground='#34495e')
        self.canvas.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(left_frame, bg=self.colors['panel_bg'])
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        stats_text = [
            f"Steps: {self.steps}",
            f"Undone: {self.undone_steps}",
            f"Total: {self.steps + self.undone_steps}",
            f"Efficiency: -"
        ]
        
        self.stats_labels = []
        for i, text in enumerate(stats_text):
            label = tk.Label(stats_frame, text=text, font=('Arial', 14), 
                           fg='white', bg=self.colors['panel_bg'])
            label.grid(row=0, column=i, padx=20, pady=5)
            self.stats_labels.append(label)
        
        # BFS controls
        bfs_frame = tk.Frame(left_frame, bg=self.colors['bg_dark'])
        bfs_frame.pack(pady=10)
        
        tk.Button(bfs_frame, text="Start BFS", command=self.start_bfs,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(bfs_frame, text="Next Step", command=self.bfs_step,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(bfs_frame, text="Reset BFS", command=self.reset_bfs,
                 font=('Arial', 10), bg='#e74c3c', fg='white').pack(side='left', padx=5)
        
        # Right frame for controls
        right_frame = tk.Frame(content_frame, bg=self.colors['bg_dark'])
        right_frame.pack(side='right', fill='y', padx=20)
        
        # Movement controls
        control_frame = tk.Frame(right_frame, bg=self.colors['panel_bg'])
        control_frame.pack(pady=10, fill='x')
        
        # Direction buttons
        tk.Button(control_frame, text="Move Up", command=lambda: self.move('up'),
                 font=('Arial', 12), bg='#3498db', fg='white', width=15).pack(pady=5)
        
        dir_frame = tk.Frame(control_frame, bg=self.colors['panel_bg'])
        dir_frame.pack(pady=5)
        tk.Button(dir_frame, text="Move Left", command=lambda: self.move('left'),
                 font=('Arial', 12), bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(dir_frame, text="Move Right", command=lambda: self.move('right'),
                 font=('Arial', 12), bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Move Down", command=lambda: self.move('down'),
                 font=('Arial', 12), bg='#3498db', fg='white', width=15).pack(pady=5)
        
        # Action buttons
        tk.Button(right_frame, text="Undo Last Move", command=self.undo_move,
                 font=('Arial', 12), bg='#e67e22', fg='white', width=20).pack(pady=5)
        tk.Button(right_frame, text="Reset Game", command=self.reset_game,
                 font=('Arial', 12), bg='#e74c3c', fg='white', width=20).pack(pady=5)
        tk.Button(right_frame, text="Show All Paths", command=self.show_all_paths,
                 font=('Arial', 12), bg='#9b59b6', fg='white', width=20).pack(pady=5)
        
        # Instructions
        instr_frame = tk.Frame(right_frame, bg=self.colors['panel_bg'])
        instr_frame.pack(pady=10, fill='x')
        
        instr_text = """How to Play:
• Use arrow keys or buttons to move
• Find shortest path from Start to End
• Use Undo if you make wrong move
• Try to find optimal path
• Use BFS to see algorithm"""
        
        instr_label = tk.Label(instr_frame, text=instr_text, font=('Arial', 10), 
                              fg='white', bg=self.colors['panel_bg'], justify='left')
        instr_label.pack(padx=10, pady=10)
        
        # Path info (will be updated after calculation)
        self.path_frame = tk.Frame(left_frame, bg=self.colors['bg_dark'])
        self.path_frame.pack(pady=10)
        
        self.path_labels = []
        
        # Bind keyboard events
        self.root.bind('<Up>', lambda e: self.move('up'))
        self.root.bind('<Down>', lambda e: self.move('down'))
        self.root.bind('<Left>', lambda e: self.move('left'))
        self.root.bind('<Right>', lambda e: self.move('right'))
        self.root.bind('<Control-z>', lambda e: self.undo_move())
    
    def update_path_display(self):
        """Update the path information display with calculated values"""
        # Clear existing path labels
        for widget in self.path_frame.winfo_children():
            widget.destroy()
        
        path_details = [
            ("Best Path", self.paths["best"], '#2ecc71'),
            ("Average Path", self.paths["avg"], '#3498db'),
            ("Worst Path", self.paths["worst"], '#e74c3c')
        ]
        
        for i, (name, steps, color) in enumerate(path_details):
            frame = tk.Frame(self.path_frame, bg=color, relief='raised', bd=2)
            frame.grid(row=0, column=i, padx=10)
            
            tk.Label(frame, text=name, font=('Arial', 10, 'bold'), 
                    bg=color, fg='white').pack(padx=10, pady=2)
            tk.Label(frame, text=f"Steps: {steps}", font=('Arial', 9), 
                    bg=color, fg='white').pack(padx=10)
            tk.Label(frame, text="O(V+E)", font=('Arial', 9), 
                    bg=color, fg='white').pack(padx=10, pady=2)
        
    def initialize_maze(self):
        # Create empty maze filled with walls
        self.maze = [[1 for _ in range(self.maze_size)] for _ in range(self.maze_size)]
        
        # Manually design a complex maze with three clear paths
        # MODIFIED: Connected row 2, col 11 with row 2, col 10
        maze_design = [
            # Row 0-14, Col 0-14
            # 1 = wall, 0 = path
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 0
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],  # 1 - Start at (1,1)
            [1,1,1,0,1,0,1,1,1,0,0,0,1,0,1],  # 2 - MODIFIED: Connected (2,10) and (2,11)
            [1,0,1,0,0,0,1,0,0,0,1,0,1,0,1],  # 3
            [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],  # 4
            [1,0,0,0,0,1,1,0,1,0,1,0,1,0,1],  # 5
            [1,0,1,1,0,1,1,0,1,0,1,1,1,0,1],  # 6
            [1,0,1,0,0,0,1,0,1,0,0,0,0,0,1],  # 7
            [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],  # 8
            [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],  # 9
            [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],  # 10
            [1,0,1,0,0,0,0,0,0,0,1,0,1,0,1],  # 11
            [1,0,1,1,1,1,1,1,1,0,1,0,1,0,1],  # 12
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],  # 13 - End at (13,13)
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]   # 14
        ]
        
        # Convert design to maze
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                self.maze[i][j] = maze_design[i][j]
        
        # Set start and end positions
        self.maze[self.start_position[0]][self.start_position[1]] = 2
        self.maze[self.end_position[0]][self.end_position[1]] = 3
    
    def calculate_path_lengths(self):
        """Calculate the actual path lengths using BFS and path analysis"""
        print("Calculating path lengths...")
        
        # Find shortest path using BFS
        shortest_length = self.find_shortest_path()
        
        # Estimate other path lengths based on maze structure
        # These are educated guesses based on the maze design
        self.paths["best"] = shortest_length
        self.paths["avg"] = shortest_length + 8   # Medium path
        self.paths["worst"] = shortest_length + 16  # Longest path
        
        print(f"Calculated paths - Best: {self.paths['best']}, Avg: {self.paths['avg']}, Worst: {self.paths['worst']}")
        
        # Update the display
        self.update_path_display()
    
    def find_shortest_path(self):
        """Use BFS to find the actual shortest path length"""
        queue = deque([self.start_position])
        visited = {self.start_position}
        parent = {self.start_position: None}
        
        while queue:
            current = queue.popleft()
            
            if current == self.end_position:
            
                path = []
                temp = current
                while temp is not None:
                    path.append(temp)
                    temp = parent[temp]
                return len(path) - 1 
            
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = current[0] + dr, current[1] + dc
                new_pos = (new_row, new_col)
                
                if (0 <= new_row < self.maze_size and 0 <= new_col < self.maze_size and
                    new_pos not in visited and
                    (self.maze[new_row][new_col] in [0, 2, 3])):
                    
                    queue.append(new_pos)
                    visited.add(new_pos)
                    parent[new_pos] = current
        
        return 0  
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        for row in range(self.maze_size):
            for col in range(self.maze_size):
                x1 = col * self.cell_size + 5
                y1 = row * self.cell_size + 5
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_value = self.maze[row][col]
                
                if cell_value == 1:  # Wall
                    color = self.colors['wall']
                elif cell_value == 2:  # Start
                    color = self.colors['start']
                elif cell_value == 3:  # End
                    color = self.colors['end']
                elif cell_value == 0:  # Path
                    color = self.colors['path']
                else:
                    color = self.colors['wall']
                
                # Draw cell
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                
                # Draw BFS visited
                if (row, col) in self.bfs_visited:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors['visited'])
                
                # Draw shortest path
                if (row, col) in self.shortest_path and (row, col) != self.start_position and (row, col) != self.end_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors['shortest'])
                
                # Draw current position
                if (row, col) == self.current_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors['current'])
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="P", 
                                          font=('Arial', 12, 'bold'))
                
                # Draw start/end labels
                if cell_value == 2:  # Start
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="S", 
                                          font=('Arial', 12, 'bold'), fill='white')
                elif cell_value == 3:  # End
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="E", 
                                          font=('Arial', 12, 'bold'), fill='white')
    
    def move(self, direction):
        if self.game_completed:
            return
        
        row, col = self.current_position
        new_row, new_col = row, col
        
        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1
        
        # Check if move is valid (path, start, or end)
        if (0 <= new_row < self.maze_size and 0 <= new_col < self.maze_size and
            (self.maze[new_row][new_col] in [0, 2, 3])):
            
            self.move_history.append((row, col))
            self.current_position = (new_row, new_col)
            self.steps += 1
            self.update_stats()
            
            if self.current_position == self.end_position:
                self.game_completed = True
                self.show_result()
            
            self.draw_maze()
    
    def undo_move(self):
        if self.move_history and not self.game_completed:
            self.current_position = self.move_history.pop()
            self.undone_steps += 1
            self.update_stats()
            self.draw_maze()
    
    def reset_game(self):
        self.current_position = self.start_position
        self.steps = 0
        self.undone_steps = 0
        self.move_history = []
        self.game_completed = False
        self.reset_bfs()
        self.update_stats()
        self.draw_maze()
    
    def start_bfs(self):
        self.bfs_running = True
        self.bfs_queue = deque([self.start_position])
        self.bfs_visited = {self.start_position}
        self.bfs_parent = {self.start_position: None}
        self.shortest_path = []
        self.draw_maze()
    
    def bfs_step(self):
        if not self.bfs_running or not self.bfs_queue:
            self.bfs_running = False
            return
        
        current = self.bfs_queue.popleft()
        
        if current == self.end_position:
            self.highlight_shortest_path(current)
            self.bfs_running = False
            return
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = current[0] + dr, current[1] + dc
            new_pos = (new_row, new_col)
            
            if (0 <= new_row < self.maze_size and 0 <= new_col < self.maze_size and
                new_pos not in self.bfs_visited and
                (self.maze[new_row][new_col] in [0, 2, 3])):
                
                self.bfs_queue.append(new_pos)
                self.bfs_visited.add(new_pos)
                self.bfs_parent[new_pos] = current
        
        self.draw_maze()
    
    def highlight_shortest_path(self, end_pos):
        current = end_pos
        self.shortest_path = []
        
        while current is not None:
            self.shortest_path.append(current)
            current = self.bfs_parent.get(current)
        
        self.shortest_path.reverse()
        
        # Calculate actual shortest path length
        actual_steps = len(self.shortest_path) - 1
        print(f"BFS found shortest path with {actual_steps} steps")
        
        # Update the best path if BFS found a shorter one
        if actual_steps < self.paths["best"]:
            self.paths["best"] = actual_steps
            self.update_path_display()
        
        self.draw_maze()
    
    def reset_bfs(self):
        self.bfs_running = False
        self.bfs_visited.clear()
        self.bfs_queue.clear()
        self.bfs_parent.clear()
        self.shortest_path = []
        self.draw_maze()
    
    def show_all_paths(self):
        self.start_bfs()
        # Complete BFS in one go
        while self.bfs_running:
            self.bfs_step()
            self.root.update()
            time.sleep(0.1)
    
    def update_stats(self):
        efficiency = "-"
        if self.game_completed:
            if self.steps <= self.paths["best"]:
                efficiency = "Perfect"
            elif self.steps <= self.paths["avg"]:
                efficiency = "Good"
            elif self.steps <= self.paths["worst"]:
                efficiency = "Average"
            else:
                efficiency = "Poor"
        
        stats_text = [
            f"Steps: {self.steps}",
            f"Undone: {self.undone_steps}",
            f"Total: {self.steps + self.undone_steps}",
            f"Efficiency: {efficiency}"
        ]
        
        for i, text in enumerate(stats_text):
            self.stats_labels[i].config(text=text)
    
    def show_result(self):
        if self.steps <= self.paths["best"]:
            message = f"Perfect! You found the shortest path in {self.steps} steps!"
        elif self.steps <= self.paths["avg"]:
            message = f"Good! You completed in {self.steps} steps. Best is {self.paths['best']}."
        elif self.steps <= self.paths["worst"]:
            message = f"Average performance. You took {self.steps} steps. Try to find a shorter path!"
        else:
            message = f"You took {self.steps} steps. The optimal path is only {self.paths['best']} steps."
        
        messagebox.showinfo("Maze Completed!", message)

if __name__ == "__main__":
    root = tk.Tk()
    game = BFSMazeExplorer(root)
    root.mainloop()