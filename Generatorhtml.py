import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

# Function to generate HTML from the article
def generate_html():
    api_key = entry_api_key.get()
    file_path = entry_file_path.get()
    save_directory = entry_save_directory.get()

    if not api_key:
        messagebox.showerror("Error", "Proszę podać swój klucz do OpenAI API.")
        return
    if not file_path:
        messagebox.showerror("Error", "Proszę wybrać plik z artykułem.")
        return
    if not save_directory:
        messagebox.showerror("Error", "Proszę wybrać gdzie zapisać wygenerowany plik.")
        return

    # Set the output file path to "artykul.html" in the chosen directory
    output_file_path = os.path.join(save_directory, "artykul.html")

    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Read the article content from the file
        with open(file_path, "r", encoding="utf-8") as file:
            article_content = file.read()

        # Define the prompt
        prompt = f"""
        Przekształć poniższy artykuł do kodu HTML, który zawiera odpowiednią strukturę:
        - użyj odpowiednich tagów HTML,
        - dodaj miejsca na grafiki z tagiem <img src="image_placeholder.jpg" alt="Opis grafiki">,
        - dodaj podpisy pod obrazkami używając odpowiedniego tagu <figure>,
        - nie używaj CSS ani JavaScriptu, zwróć tylko kod HTML do wstawienia pomiędzy tagami <body> i </body>, nie dołączaj znaczników <html>,
        <head> ani <body>.

        Artykuł:
        {article_content}
        """

        # Send request to OpenAI API and get the response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the generated HTML
        generated_html = response.choices[0].message.content

        # Remove ```html markers if present
        if generated_html.startswith("```html"):
            generated_html = generated_html[7:]  # Remove initial ```html
        if generated_html.endswith("```"):
            generated_html = generated_html[:-3]  # Remove trailing ```

        # Save the generated HTML to the chosen file path
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(generated_html)

        messagebox.showinfo("Success", f"Plik HTML został zapisany jako {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Coś poszło nie tak: {e}")

# Function to select the article file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

# Function to select the save directory
def select_directory():
    directory_path = filedialog.askdirectory()
    entry_save_directory.delete(0, tk.END)
    entry_save_directory.insert(0, directory_path)

# Main application window
app = tk.Tk()
app.title("Generator artykulu HTML")
app.geometry("400x300")

# Label and entry for the API key
label_api_key = tk.Label(app, text="OpenAI API klucz:")
label_api_key.pack()
entry_api_key = tk.Entry(app, show="*", width=50)
entry_api_key.pack()

# Label and button to select the article file
label_file_path = tk.Label(app, text="Plik artykułu (.txt):")
label_file_path.pack()
entry_file_path = tk.Entry(app, width=50)
entry_file_path.pack()
button_browse = tk.Button(app, text="Wybierz plik", command=select_file)
button_browse.pack()

# Label and button to select the save directory
label_save_directory = tk.Label(app, text="Gdzie zapisać plik:")
label_save_directory.pack()
entry_save_directory = tk.Entry(app, width=50)
entry_save_directory.pack()
button_directory = tk.Button(app, text="Wybierz folder", command=select_directory)
button_directory.pack()

# Button to generate HTML - make it a little bigger and lower
button_generate = tk.Button(app, text="Generuj HTML", command=generate_html, height=3, width=20)  # Adjust height and width
button_generate.pack(pady=20)  # Added more padding to push it lower

# Run the application
app.mainloop()
