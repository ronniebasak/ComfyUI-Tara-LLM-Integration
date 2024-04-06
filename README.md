# Tara - ComfyUI Node for LLM Integration

<p align="center">
  <img src="logo/tara-logo.webp" alt="Tara Logo" width="200"/>
</p>

## Introduction
Tara is a powerful node for ComfyUI that integrates Large Language Models (LLMs) to enhance and automate workflow processes. With Tara, you can create complex, intelligent workflows that refine and generate content, manage API keys, and seamlessly integrate various LLMs into your projects.

## Features
Tara comprises four main nodes:

- **TaraPrompter**: Utilizes input guidance to generate refined positive and negative outcomes.
- **TaraApiKeyLoader**: Manages and loads saved API keys for different LLM services.
- **TaraApiKeySaver**: Provides a secure way to save and store API keys internally.
- **TaraDaisyChainNode**: Enables complex workflows by allowing outputs to be daisy-chained into subsequent prompts, facilitating intricate operations like checklist creation, verification, execution, evaluation, and refinement.

Currently, Tara supports OpenAI and Grok (all models), with plans to expand support to together.ai and Replicate.

## Installation
Tara can be installed using one of the following methods:

### Method 1:
1. Navigate to the `custom_nodes` directory inside the ComfyUI root folder, typically found at `/workspace/ComfyUI/custom_nodes` in Runpod.
2. Clone this repository using `git clone <repository-url>`.
3. Restart ComfyUI and reload your browser to apply changes.

### Method 2: (Prerequisite: ComfyUI manager)
1. Open ComfyUI Manager.
2. Click "Install via Git URL".
3. Paste the link of this repository.
4. Restart ComfyUI and reload your browser to apply changes.

## Usage
### TaraPrompter
- **Input**: Guidance, Positive, Negative
- **Output**: Refined Positive, Refined Negative

### TaraApiKeyLoader
Loads and provides API keys for other Tara nodes.

### TaraApiKeySaver
Securely saves API keys used by Tara nodes.

### TaraDaisyChainNode
- **Input**: Guidance, Prompt, Positive, Negative
- **Output**: Generated text, suitable for chaining in workflows.

## Future Plans
- Integration with together.ai for collaborative LLM usage.
- Support for Replicate, enabling access to a broader range of AI models.

## Contributing
We welcome contributions to Tara! If you have suggestions or improvements, please fork the repository and submit a pull request.

## Disclaimer
When using Tara with a hosted ComfyUI service, there is an option to save the API key temporarily. This action stores the key in the `/tmp` directory, which is typically auto-deleted on Linux-based systems. However, this might pose a risk if the server is shared among multiple users, as one person's API key could potentially overwrite another's. As Tara is in its alpha version, addressing bugs is our priority. In the meantime, users may opt to input the API key as a text (or primitive) node; this method ensures the API key is never saved on the server. When using a primitive node, remember to collapse it during screen recording or sharing to protect your API key.

## License
Tara is released under the GNU General Public License v3.0 (GPLv3).