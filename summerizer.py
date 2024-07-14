#requirements, use pip to install these requirements
import click
import requests

#I dowmloaded qwen2 model using ollama so make sure u have the qwen2 model running using ollama
#model serving locally so using ollama on port 11434
API_URL = 'http://localhost:11434/api/generate'

def summarize_text(text):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'qwen2',
        'prompt': f"Please summarize the following text: {text}",
        'stream': False 
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('response','no summary found')  # Assuming the result contains the summary or else returning no summary found
    except requests.exceptions.RequestException as e:
        return f'error: {e}'

@click.command(name='QuickSummarize')
@click.option('--file', type=click.File('r'), help='Path to the text file.')
@click.option('--text', type=str, help='Text')
def main(file, text):
    sample_text = "This is a sample text that provides an example of how the summarization tool works. Summarization tools can be incredibly useful for quickly extracting key information from large amounts of text."
    if file:
        text_to_summarize = file.read()
    elif text:
        text_to_summarize = text
    else:
        click.echo('No input provided. Using sample text.')
        text_to_summarize = sample_text
    
    summary = summarize_text(text_to_summarize)
    click.echo(f'Summary:\n{summary}')

if __name__ == '__main__':
    main()

##To test this script
##install the requirements
# python run summerizer.py ==> it uses sample text in the script itself when no text or path to text file is provided
## python run summerizer.py --text "The Industrial Revolution, which took place from the 18th to 19th centuries" ===> to test using text

## pythonn run summerizer.py --file sample1.txt ==>to test using text file, sample text files are attacthed to this script