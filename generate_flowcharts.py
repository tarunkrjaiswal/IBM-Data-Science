import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart(steps, filename, title):
    fig, ax = plt.subplots(figsize=(6, len(steps)*1.5))
    ax.axis('off')
    
    # Coordinates
    box_width = 0.8
    box_height = 0.6
    x_center = 0.5
    y_starts = [len(steps) - i for i in range(len(steps))]
    
    for i, step in enumerate(steps):
        # Draw Box
        rect = patches.FancyBboxPatch(
            (x_center - box_width/2, y_starts[i] - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.1",
            edgecolor='black', facecolor='lightblue', lw=2
        )
        ax.add_patch(rect)
        
        # Add Text
        ax.text(x_center, y_starts[i], step, ha='center', va='center', fontsize=12, wrap=True)
        
        # Draw Arrow
        if i < len(steps) - 1:
            ax.annotate('', xy=(x_center, y_starts[i+1] + box_height/2 + 0.1), 
                        xytext=(x_center, y_starts[i] - box_height/2 - 0.1),
                        arrowprops=dict(arrowstyle="->", lw=2))
            
    plt.title(title, fontsize=16, pad=20)
    plt.xlim(0, 1)
    plt.ylim(0.5, len(steps) + 0.5)
    plt.savefig(f"plots/{filename}", bbox_inches='tight')
    plt.close()

# Slide 8
api_steps = [
    "1. Request Data\n(api.spacexdata.com/v4/launches)",
    "2. Receive JSON Response",
    "3. Use json_normalize()\nto convert to DataFrame",
    "4. Extract Custom Features\n(Rocket, Payload, Cores)",
    "5. Filter Data\n(Falcon 9 launches only)"
]
draw_flowchart(api_steps, "api_flowchart.png", "SpaceX API Data Collection Process")

# Slide 9
scraping_steps = [
    "1. Request HTML Page\n(Wikipedia: Falcon 9 Launches)",
    "2. Parse HTML\n(BeautifulSoup)",
    "3. Extract Table Elements\n(Find <th> and <td> tags)",
    "4. Iterate Rows\n(Extract Launch details)",
    "5. Store as DataFrame\n& Clean Dictionary"
]
draw_flowchart(scraping_steps, "scraping_flowchart.png", "Web Scraping Process")

print("Flowcharts generated.")
