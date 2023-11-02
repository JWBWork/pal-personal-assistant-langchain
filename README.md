# PAL - Personal Assistant Langchain

PAL is an experimental project that uses Langchain's structured tools to manage todos through a natural language interface integrated with Notion.

## Technologies Used

- Python
- Langchain
- Notion SDK
- OpenAI

## Installation and Running the Project

Before running the project, you need to set up a few things:

1. **Install the required packages** from `requirements.txt` using pip:

```bash
pip install -r requirements.txt
```

2. **Set up the environment variables**:

- `OPENAI_API_KEY`: This is your OpenAI API key, which is used to authenticate with the OpenAI API. You can find more information on how to get your OpenAI API key in the [OpenAI API documentation](https://beta.openai.com/docs/developer-quickstart/).

- `NOTION_TOKEN`: This is your Notion token, which is used to authenticate with the Notion API. You can find more information on how to get your Notion token in the [Notion API documentation](https://developers.notion.com/docs/getting-started).

- `DATABASE_ID`: This is the ID of your Notion database where the todos are stored. You can find this ID by opening your Notion database and copying the ID from the URL.


3. **Run the project** with the following command:

```bash
python main.py
```

For detailed logging from Langchain, you can use the --verbose flag:

```bash
python main.py --verbose
```

## Shortcomings and Future Work

Currently, there are a few shortcomings in the project. For instance, the Langchain Language Model (LLM) occasionally lies and does not use tools effectively. It will hallucinate tool responses instead of using the tools to get the desired response. This can be mitigated to some degree through prompt engineering tool descriptions.

When using certian tools may get caught in a loop where the LLM will keep using the same tool over and over again. The agent will often fire tools off multiple times before doing something productive with the response.

Earlier experiments used a custom Notion document loader which created a vector database of all the todos in the Notion database as documents. This was useful for finding best matching todos with FAISS. Removed as unnecessary and introduced complexity keeping it in sync with the Notion database. Might re-introduce as a better way to find best todo IDs when one is needed without relying on the LLM to parse the list of todos.

## Contribution

Feel free to contribute to the project by submitting a pull request.

## License

This project is licensed under the terms of the MIT license.