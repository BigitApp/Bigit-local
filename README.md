<a name="readme-top"></a>

[![Twitter][twitter-shield]][twitter-url]

<br />
<div align="center">
  <a href="https://bigitapp.com/">
    <img src="frontend/public/logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Bigit-local</h1>

  <p align="center">
     Blockchain And AI Generate Your Individual AI BOT
    <br />
    <a href="https://github.com/BigitApp"><strong>Explore in github »</strong></a>
    <br />
    <br />
    <a href="https://bigitapp.com/">View Demo</a>
    ·
    <a href="mailto:support@bigitapp.com">Report Bug</a>
  </p>
</div>

> Bigit-local consists of the back end and the front end.

## Backend

1. **Download the Model File**
   - Download the model file from Hugging Face and place it into the `llms` folder.

2. **Set Up the Environment**
   - Install dependencies with Poetry:
     ```bash
     poetry install
     ```
   - Activate the Poetry shell:
     ```bash
     poetry shell
     ```
   - Install additional packages for BigDL LLM with pip:
     ```bash
     !pip install bigdl-llm[all]
     ```

3. **Run the Development Server**
   - Start the server with:
     ```bash
     python main.py
     ```

4. **Access the API Documentation**
   - Open http://localhost:8000/docs in your browser to view the Swagger UI of the API.

## Frontend

1. **Set Up the Environment**
   - Install project dependencies with PNPM:
     ```bash
     pnpm install
     ```

2. **Run the Frontend**
   - Start the development server with:
     ```bash
     npm run dev
     ```

## Acknowledgements

We would like to express our gratitude to the creators of the [chat-llamaindex](https://github.com/run-llama/chat-llamaindex) repository for providing valuable reference code. Their work has been instrumental in the development of this project.




[license-shield]: https://img.shields.io/github/license/AAooWW/Bigit?style=for-the-badge
[license-url]: https://github.com/AAooWW/Bigit/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/follow/Bigit?style=social
[twitter-url]: https://x.com/BigitDapp