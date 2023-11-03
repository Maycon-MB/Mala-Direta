import PySimpleGUI as sg
from fpdf import FPDF

def create_pdf(items):
    # Initialize the PDF document
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    # Set the font for the document
    pdf.set_font("Arial", size=12)

    # Initialize the count of rectangles
    rectangle_count = 0

    # Initialize the page count
    page_count = 1

    # Loop through each item in the database
    for item in items:
        # Add the item to the current page
        pdf.cell(40, 10, txt=item, ln=True)

        # Increment the rectangle count
        rectangle_count += 1

        # Check if the rectangle count has reached the limit of 27
        if rectangle_count == 27:
            # Add the current page to the PDF document
            pdf.output(f"page_{page_count}.pdf")

            # Create a new page
            pdf.add_page()

            # Reset the rectangle count
            rectangle_count = 0

            # Increment the page count
            page_count += 1

    # Check if there are remaining items on the last page
    if rectangle_count > 0:
        # Add the last page to the PDF document
        pdf.output(f"page_{page_count}.pdf")

    # Return the PDF document
    return pdf

# Retrieve items from the database
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10", "Item 11", "Item 12", "Item 13", "Item 14", "Item 15", "Item 16", "Item 17", "Item 18", "Item 19", "Item 20", "Item 21", "Item 22", "Item 23", "Item 24", "Item 25", "Item 26", "Item 27", "Item 28", "Item 29", "Item 30"]

# Create the PDF document
pdf = create_pdf(items)

# Show the PDF document
pdf.output("output.pdf")

def generate_rectangles(data):
    items_per_page = 27
    num_pages = -(-len(data) // items_per_page)  # Ceiling division to get the number of pages

    for page in range(num_pages):
        layout = []
        start_index = page * items_per_page
        end_index = min(start_index + items_per_page, len(data))
        page_data = data[start_index:end_index]

        for item in page_data:
            layout.append([sg.Text(item)])

        # Create the window
        window = sg.Window(f"Page {page+1}", layout)

        # Event loop
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break

        window.close()

# Example usage
data = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10",
        "Item 11", "Item 12", "Item 13", "Item 14", "Item 15", "Item 16", "Item 17", "Item 18", "Item 19", "Item 20",
        "Item 21", "Item 22", "Item 23", "Item 24", "Item 25", "Item 26", "Item 27", "Item 28", "Item 29"]

generate_rectangles(data)