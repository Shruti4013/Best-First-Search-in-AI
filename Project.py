import heapq
import tkinter as tk
from tkinter import simpledialog, messagebox

graph = {}

def best_first_search(graph, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    visited = set()
    parent = {start: None}
    
    while priority_queue:
        cost, current = heapq.heappop(priority_queue)
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        visited.add(current)
        
        for neighbor, heuristic in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (heuristic, neighbor))
                parent[neighbor] = current
    return None

def reconstruct_path(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]

def start_app():
    first_window = tk.Tk()
    first_window.title("Graph Setup")
    first_window.configure(bg="lavender")
    first_window.geometry("400x200")

    tk.Label(first_window, text="Enter number of labels in graph:", font=("Arial", 12, "bold"), bg="lavender").pack(pady=10)
    num_nodes_entry = tk.Entry(first_window, font=("Arial", 12))
    num_nodes_entry.pack()

    def proceed():
        try:
            num = int(num_nodes_entry.get())
            first_window.destroy()
            enter_nodes(num)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number")

    tk.Button(first_window, text="Next", font=("Arial", 12, "bold"), bg="blue", fg="white", command=proceed).pack(pady=20)
    first_window.mainloop()

def enter_nodes(num_nodes):
    node_data_window = tk.Tk()
    node_data_window.title("Enter Graph Details")
    node_data_window.configure(bg="honeydew")
    node_data_window.geometry("600x600")

    entries = []

    tk.Label(node_data_window, text="Enter node and its adjacent nodes with heuristic\nFormat: A -> B:4,C:2", font=("Arial", 10), bg="honeydew", fg="darkgreen").pack(pady=10)

    for i in range(num_nodes):
        frame = tk.Frame(node_data_window, bg="honeydew")
        frame.pack(pady=5)
        tk.Label(frame, text=f"Node {i + 1}:", bg="honeydew", font=("Arial", 10)).pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=50)
        entry.pack(side=tk.LEFT)
        entries.append(entry)

    def build_graph():
        global graph
        graph.clear()
        try:
            for entry in entries:
                text = entry.get().strip()
                if "->" not in text:
                    raise ValueError
                node, rest = text.split("->")
                node = node.strip()
                connections = rest.strip().split(",")
                graph[node] = []
                for conn in connections:
                    n, h = conn.strip().split(":")
                    graph[node].append((n.strip(), int(h.strip())))
            node_data_window.destroy()
            show_search_gui()
        except:
            messagebox.showerror("Error", "Invalid format. Please use format like A -> B:4,C:2")

    tk.Button(node_data_window, text="Next", font=("Arial", 12, "bold"), bg="blue", fg="white", command=build_graph).pack(pady=20)

    node_data_window.mainloop()

def show_search_gui():
    search_window = tk.Tk()
    search_window.title("Best-First Search")
    search_window.configure(bg="lightyellow")
    search_window.geometry("500x300")

    tk.Label(search_window, text="Enter Start Node:", font=("Arial", 12, "bold"), bg="lightyellow").pack(pady=5)
    start_entry = tk.Entry(search_window, font=("Arial", 12))
    start_entry.pack()

    tk.Label(search_window, text="Enter Goal Node:", font=("Arial", 12, "bold"), bg="lightyellow").pack(pady=5)
    goal_entry = tk.Entry(search_window, font=("Arial", 12))
    goal_entry.pack()

    result_label = tk.Label(search_window, text="", font=("Arial", 14, "bold"), bg="lightyellow")
    result_label.pack(pady=20)

    def run_search():
        start = start_entry.get().strip()
        goal = goal_entry.get().strip()
        if start not in graph or goal not in graph:
            messagebox.showerror("Error", "Start or goal node not found in graph.")
            return
        path = best_first_search(graph, start, goal)
        if path:
            result_label.config(text=f"Shortest Path: {' -> '.join(path)}", fg="green")
        else:
            result_label.config(text="No path found.", fg="red")

    tk.Button(search_window, text="Find Path", font=("Arial", 12, "bold"), bg="darkgreen", fg="white", command=run_search).pack(pady=10)

    search_window.mainloop()

start_app()