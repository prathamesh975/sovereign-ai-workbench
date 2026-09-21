\# Sovereign AI Workbench



A local-first Agentic AI Workbench designed for confidential industrial knowledge work.



\## Overview



The system processes documents locally, retrieves relevant organizational knowledge, uses a locally hosted LLM for reasoning and generation, and validates the generated output before returning it to the user.



\## Tech Stack



\### Frontend

\- React

\- TypeScript

\- Tailwind CSS

\- Vite



\### Backend

\- Python

\- FastAPI



\### AI / Agent Runtime

\- Ollama

\- Qwen2.5-Coder 3B

\- Custom Agent orchestration

\- Planner

\- Context Manager

\- Execution Loop

\- Validator



\### RAG \& Document Intelligence

\- ChromaDB

\- PyMuPDF

\- OCR processing

\- Local document retrieval



\## Key Features



\- Local-first AI processing

\- Document upload and analysis

\- Retrieval-Augmented Generation (RAG)

\- Local organizational knowledge base

\- Agent-based task execution

\- Document-aware generation

\- Output validation

\- Local LLM inference through Ollama

\- Designed for confidential industrial workflows



\## Agent Workflow



The current agent workflow is:



1\. Read the input document

2\. Extract relevant information

3\. Search the local knowledge base

4\. Analyze the findings

5\. Generate the requested deliverable

6\. Validate the output



\## Architecture



```text

User

&#x20; |

&#x20; v

React + Tailwind Frontend

&#x20; |

&#x20; v

FastAPI Backend

&#x20; |

&#x20; v

Agent Orchestration

&#x20; |

&#x20; +-------------------+

&#x20; |                   |

&#x20; v                   v

Document Processing   Local RAG

PyMuPDF / OCR        ChromaDB

&#x20; |                   |

&#x20; +---------+---------+

&#x20;           |

&#x20;           v

&#x20;     Ollama Runtime

&#x20;           |

&#x20;           v

&#x20;    Qwen2.5-Coder 3B

&#x20;           |

&#x20;           v

&#x20;       Validator

&#x20;           |

&#x20;           v

&#x20;      Final Output

