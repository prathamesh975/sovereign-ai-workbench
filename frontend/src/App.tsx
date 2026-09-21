import { useState } from "react";
import ReactMarkdown from "react-markdown";

const API_URL = "http://127.0.0.1:8000";

type ExecutionStep = {
  step: number;
  action: string;
  result?: string;
};

type ValidationInfo = {
  passed?: boolean;
  checks?: Record<string, boolean>;
  missing_sections?: string[];
  placeholders?: string[];
  issues?: string[];
  detail?: string;
} | string | null;

function App() {
  const [task, setTask] = useState(
    "Analyze the inspection report and prepare an approval note."
  );

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePath, setFilePath] = useState("");

  const [uploading, setUploading] = useState(false);
  const [running, setRunning] = useState(false);

  const [output, setOutput] = useState("");
  const [validation, setValidation] = useState<ValidationInfo>(null);

  const [execution, setExecution] = useState<ExecutionStep[]>([]);
  const [sources, setSources] = useState<any[]>([]);

  const [error, setError] = useState("");

  // --------------------------------------------------
  // Upload document
  // --------------------------------------------------

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setError("");
    setOutput("");
    setValidation(null);
    setExecution([]);
    setSources([]);
    setFilePath("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setFilePath(data.file_path);

    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong during upload"
      );
      setSelectedFile(null);
    } finally {
      setUploading(false);
    }
  };

  // --------------------------------------------------
  // Run Agent
  // --------------------------------------------------

  const handleDownload = () => {
    if (!output) {
      return;
    }

     const blob = new Blob([output], {
      type: "text/markdown;charset=utf-8",
      });

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "approval_note.md";

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

  };

  const handleRunAgent = async () => {
  setError("");
  setOutput("");
  setValidation(null);
  setExecution([]);
  setSources([]);

  if (!selectedFile || !filePath) {
    setError("Please upload a document first.");
    return;
  }

  if (!task.trim()) {
    setError("Please enter a task for the AI agent.");
    return;
  }

  setRunning(true);

  try {
    console.log("[Agent] Starting request...");

    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: task,
        task_type: "general",
        file_path: filePath,
      }),
    });

    console.log("[Agent] Response received:", response.status);

    const data = await response.json();

    console.log("[Agent] Response data:", data);

    if (!response.ok) {
      throw new Error(
        data.detail || "Agent execution failed"
      );
    }

    // -----------------------------
    // Store generated output
    // -----------------------------

    setOutput(
      data.response || "No output was generated."
    );

    // -----------------------------
    // Store validation result
    // -----------------------------

    setValidation(
      data.validation !== undefined ? data.validation : (data.response ? { passed: true } : null)
    );

    // -----------------------------
    // Store execution steps
    // -----------------------------

    setExecution(
      data.execution || []
    );

    // -----------------------------
    // Store knowledge sources
    // -----------------------------

    setSources(
      data.generation_sources ||
      data.rag_sources ||
      data.analysis_sources ||
      []
    );

    console.log("[Agent] UI updated successfully.");

  } catch (err) {

    console.error("[Agent] Error:", err);

    setError(
      err instanceof Error
        ? err.message
        : "Something went wrong while running the agent."
    );

  } finally {

    // IMPORTANT:
    // Always stop the loading state.
    setRunning(false);

    console.log("[Agent] Finished.");
  }
};

  const PLAN_STEPS = [
    "Read the input document",
    "Extract relevant information",
    "Search the local knowledge base",
    "Analyze the findings",
    "Generate the requested deliverable",
    "Validate the output"
  ];

  // Helper to extract validation issues for failed state
  const getValidationIssues = (val: ValidationInfo): string[] => {
    if (!val || typeof val === "string") return [];
    const issues: string[] = [];

    if (Array.isArray(val.missing_sections) && val.missing_sections.length > 0) {
      issues.push(`Missing required sections: ${val.missing_sections.join(", ")}`);
    }
    if (Array.isArray(val.placeholders) && val.placeholders.length > 0) {
      issues.push(`Detected placeholder fields: ${val.placeholders.join(", ")}`);
    }
    if (val.checks && typeof val.checks === "object") {
      if (val.checks.output_exists === false) {
        issues.push("No output generated");
      }
      if (val.checks.sufficient_content === false) {
        issues.push("Insufficient content length (<100 characters)");
      }
      if (val.checks.measurement_preserved === false) {
        issues.push("Required technical measurement was not preserved");
      }
    }
    if (Array.isArray(val.issues) && val.issues.length > 0) {
      issues.push(...val.issues);
    }
    if (typeof val.detail === "string" && val.detail) {
      issues.push(val.detail);
    }
    return issues;
  };

  const isValidationPassed =
    typeof validation === "string"
      ? validation.toLowerCase().includes("passed")
      : validation?.passed === true;

  const isValidationFailed = validation !== null && !isValidationPassed;
  const validationIssues = getValidationIssues(validation);

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col selection:bg-primary/20 selection:text-foreground">

      {/* =====================================================
          HEADER
      ====================================================== */}
      <header className="border-b border-border bg-surface sticky top-0 z-50 shadow-2xs">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 py-3.5 sm:py-4">

          {/* Brand & Title */}
          <div className="flex items-center gap-3.5">
            <div className="flex h-10 w-10 sm:h-11 sm:w-11 shrink-0 items-center justify-center rounded-xl bg-primary text-white shadow-xs">
              <svg
                className="h-5 w-5 sm:h-6 sm:w-6"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 2.5L20 6.5V12.8C20 17.6 16.6 21.6 12 22.8C7.4 21.6 4 17.6 4 12.8V6.5L12 2.5Z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
                <path
                  d="M14.5 9H9.5C8.7 9 8 9.7 8 10.5C8 11.3 8.7 12 9.5 12H14.5C15.3 12 16 12.7 16 13.5C16 14.3 15.3 15 14.5 15H9.5"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <circle cx="12" cy="18.2" r="1.1" fill="currentColor" />
              </svg>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg sm:text-xl font-bold tracking-tight text-foreground">
                  Sovereign AI Workbench
                </h1>
                <span className="hidden sm:inline-flex items-center rounded-full bg-primary-subtle border border-primary/30 px-2 py-0.5 text-[10px] font-semibold text-primary uppercase tracking-wider">
                  Air-Gapped
                </span>
              </div>

              <p className="text-xs text-muted">
                Local-first agentic AI for confidential industrial work
              </p>
            </div>
          </div>

          {/* Status Indicators */}
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="hidden md:flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-xs text-muted">
              <span>● Local Inference</span>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-border bg-surface px-3.5 py-1.5 text-xs shadow-2xs">
              <span className="h-2 w-2 rounded-full bg-success"></span>
              <span className="font-semibold text-foreground text-xs">
                Local System Online
              </span>
            </div>
          </div>

        </div>
      </header>


      {/* =====================================================
          MAIN THREE-COLUMN GRID
      ====================================================== */}
      <main className="mx-auto grid max-w-7xl grid-cols-1 lg:grid-cols-12 gap-5 sm:gap-6 p-4 sm:p-6 items-start flex-1 w-full">

        {/* =====================================================
            LEFT PANEL — WORKSPACE
        ====================================================== */}
        <section className="lg:col-span-3 rounded-2xl border border-border bg-surface p-5 shadow-2xs space-y-5">

          {/* Section Header */}
          <div className="flex items-center justify-between border-b border-border/80 pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-6 w-6 items-center justify-center rounded bg-primary-subtle text-primary border border-primary/20">
                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </div>
              <div>
                <h2 className="text-xs font-bold uppercase tracking-wider text-foreground">
                  Workspace
                </h2>
                <p className="text-[11px] text-muted">
                  Confidential document
                </p>
              </div>
            </div>
          </div>

          {/* Upload Drop Zone */}
          <label
            htmlFor="file-upload"
            className="group relative flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-border hover:border-primary bg-background hover:bg-surface p-6 text-center transition-all duration-200"
          >
            <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl border border-border bg-surface text-primary shadow-2xs transition-transform group-hover:scale-105">
              <span className="text-2xl font-light leading-none">+</span>
            </div>

            <p className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
              {uploading ? "Uploading Document..." : "Upload Document"}
            </p>

            <p className="mt-1 text-xs text-muted">
              PDF, PNG, JPG, TIFF
            </p>

            <div className="mt-3.5 flex flex-wrap justify-center gap-1.5">
              {["PDF", "PNG", "JPG", "TIFF"].map((ext) => (
                <span key={ext} className="rounded border border-border bg-surface px-2 py-0.5 text-[10px] font-mono text-muted">
                  .{ext.toLowerCase()}
                </span>
              ))}
            </div>

            <input
              id="file-upload"
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff,.webp"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>

          {/* Selected Document Card */}
          {selectedFile && (
            <div className="rounded-xl border border-border bg-background p-4 space-y-2.5 shadow-2xs">
              <div className="flex items-center justify-between text-[11px] font-semibold uppercase tracking-wider text-muted">
                <span>Selected Document</span>
                <span className="text-[10px] font-mono text-muted">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </span>
              </div>

              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-subtle text-primary border border-primary/20">
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p className="truncate text-xs font-semibold text-foreground" title={selectedFile.name}>
                  {selectedFile.name}
                </p>
              </div>

              {filePath && (
                <div className="flex items-center gap-1.5 rounded-lg bg-success-subtle border border-success/30 px-2.5 py-1 text-xs font-semibold text-success">
                  <svg className="h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>✓ Uploaded successfully</span>
                </div>
              )}

              {uploading && (
                <div className="flex items-center gap-1.5 rounded-lg bg-warning-subtle border border-warning/30 px-2.5 py-1 text-xs font-medium text-warning animate-pulse">
                  <span>Uploading document...</span>
                </div>
              )}
            </div>
          )}

          {/* Execution Mode / Security Badge */}
          <div className="rounded-xl border border-border bg-background p-4 space-y-2 shadow-2xs">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-muted">
                Execution Mode
              </span>
              <span className="inline-flex items-center gap-1 rounded bg-success-subtle border border-success/30 px-2 py-0.5 text-[10px] font-bold text-success">
                LOCAL ONLY
              </span>
            </div>

            <p className="text-xs leading-5 text-muted">
              ● Secure local workspace — Documents and AI processing remain inside the local environment.
            </p>
          </div>

        </section>


        {/* =====================================================
            CENTER PANEL — AGENT TASK & EXECUTION
        ====================================================== */}
        <section className="lg:col-span-5 rounded-2xl border border-border bg-surface p-5 shadow-2xs space-y-5 lg:max-h-[calc(100vh-100px)] lg:overflow-y-auto">

          {/* Section Header */}
          <div className="flex items-center justify-between border-b border-border/80 pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-6 w-6 items-center justify-center rounded bg-primary-subtle text-primary border border-primary/20">
                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h2 className="text-xs font-bold uppercase tracking-wider text-foreground">
                  Agent Task
                </h2>
                <p className="text-[11px] text-muted">
                  Describe the work you want the local agent to perform
                </p>
              </div>
            </div>
          </div>

          {/* Task Command Textarea */}
          <div className="relative">
            <textarea
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="Describe the work you want the local agent to perform..."
              className="h-32 w-full resize-none rounded-xl border border-border bg-surface p-4 text-sm leading-relaxed text-foreground placeholder:text-neutral outline-none transition duration-200 focus:border-primary focus:ring-1 focus:ring-primary shadow-2xs"
            />
            <div className="absolute bottom-2.5 right-3 text-[10px] font-mono text-muted">
              {task.length} chars
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="flex items-start gap-2 rounded-xl border border-error/30 bg-error-subtle p-3 text-xs font-medium text-error">
              <svg className="h-4 w-4 shrink-0 text-error mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Primary CTA Button */}
          <button
            onClick={handleRunAgent}
            disabled={running || uploading || !filePath}
            className="w-full rounded-xl bg-primary px-4 py-3 font-semibold text-white transition-all duration-200 hover:bg-primary-hover active:scale-[0.99] disabled:cursor-not-allowed disabled:bg-border disabled:text-neutral shadow-xs flex items-center justify-center gap-2"
          >
            {running ? (
              <>
                <svg className="h-4 w-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>Running Agent...</span>
              </>
            ) : (
              <span>Run Agent →</span>
            )}
          </button>

          {/* Agent Execution Vertical Timeline */}
          <div className="pt-2 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-foreground flex items-center gap-2">
                <span className="flex h-2 w-2 rounded-full bg-primary"></span>
                Agent Execution
              </h3>
              <span className="text-[10px] font-mono text-muted">
                {execution.length > 0 ? `${execution.length} steps completed` : "6-step pipeline"}
              </span>
            </div>

            {/* Vertical Connected Timeline Container */}
            <div className="relative rounded-xl border border-border bg-background p-4 shadow-2xs">
              {/* Continuous vertical connecting track line */}
              <div className="absolute left-[23px] top-6 bottom-6 w-[1.5px] bg-border z-0"></div>

              {execution.length > 0 ? (
                <div className="space-y-3 relative z-10">
                  {execution.map((item, index) => {
                    const isFailed = item.result && item.result.toLowerCase().includes("failed");

                    return (
                      <div key={index} className="flex items-start gap-3 group">
                        {/* Node indicator bead */}
                        <div className="relative z-10 flex items-center justify-center mt-0.5">
                          {isFailed ? (
                            <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-error-subtle text-error border border-error/40 text-[11px] font-bold shadow-2xs">
                              !
                            </div>
                          ) : (
                            <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-success-subtle text-success border border-success/40 text-[11px] font-bold shadow-2xs">
                              ✓
                            </div>
                          )}
                        </div>

                        {/* Step details */}
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center justify-between gap-2">
                            <p className="text-xs font-semibold text-foreground">
                              {item.action || `Step ${item.step || index + 1}`}
                            </p>
                            <span className={`text-[10px] font-medium ${isFailed ? "text-error" : "text-success"}`}>
                              {isFailed ? "! failed" : "✓ completed"}
                            </span>
                          </div>

                          {item.result && (
                            <p className="mt-1 text-[11px] leading-relaxed text-muted bg-surface p-2 rounded-lg border border-border break-words">
                              {item.result}
                            </p>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : running ? (
                <div className="space-y-3 relative z-10">
                  <div className="flex items-center gap-2 rounded-lg bg-primary-subtle border border-primary/20 p-2.5 text-xs font-medium text-primary mb-3">
                    <svg className="h-3.5 w-3.5 animate-spin text-primary shrink-0" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                    <span>Executing autonomous agent loop...</span>
                  </div>

                  {PLAN_STEPS.map((stepName, index) => (
                    <div key={index} className="flex items-start gap-3 group">
                      <div className="relative z-10 flex items-center justify-center mt-0.5">
                        <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary-subtle text-primary border border-primary/40 text-[10px] font-bold animate-pulse shadow-2xs">
                          ●
                        </div>
                      </div>

                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-xs font-medium text-foreground">
                            {stepName}
                          </p>
                          <span className="text-[10px] text-primary font-medium">
                            ● in queue / processing
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-3 relative z-10">
                  {PLAN_STEPS.map((stepName, index) => (
                    <div key={index} className="flex items-start gap-3 group">
                      <div className="relative z-10 flex items-center justify-center mt-0.5">
                        <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-surface text-neutral border border-border text-[10px]">
                          ○
                        </div>
                      </div>

                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-xs text-muted">
                            {stepName}
                          </p>
                          <span className="text-[10px] text-muted">
                            ○ pending
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Knowledge Sources */}
          <div className="pt-2 space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-foreground flex items-center gap-2">
                  <span className="flex h-2 w-2 rounded-full bg-primary"></span>
                  Knowledge Sources
                </h3>
                <p className="mt-0.5 text-[11px] text-muted">
                  Retrieved from the local organizational knowledge base
                </p>
              </div>

              {sources.length > 0 && (
                <span className="rounded-full border border-border bg-background px-2.5 py-0.5 text-[10px] font-semibold text-muted">
                  {sources.length} sources
                </span>
              )}
            </div>

            {sources.length === 0 ? (
              <div className="rounded-xl border border-border bg-background p-4 text-center text-xs text-neutral">
                Relevant knowledge sources will appear here.
              </div>
            ) : (
              <div className="space-y-2.5">
                {sources.map((source, index) => {
                  const sourceName =
                    source?.source ||
                    source?.title ||
                    `Knowledge Source ${index + 1}`;

                  const sourceText =
                    typeof source === "string"
                      ? source
                      : source?.text ||
                        source?.content ||
                        source?.document ||
                        "";

                  return (
                    <div
                      key={index}
                      className="rounded-xl border border-border bg-background p-3.5 transition hover:border-primary/40 shadow-2xs"
                    >
                      <div className="flex items-start gap-3">
                        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-primary/20 bg-primary-subtle text-xs font-bold text-primary">
                          KB
                        </div>

                        <div className="min-w-0 flex-1">
                          <div className="flex items-center justify-between gap-2">
                            <p className="text-xs font-semibold text-foreground truncate">
                              {sourceName}
                            </p>
                            <span className="text-[10px] font-medium text-success bg-success-subtle border border-success/30 px-2 py-0.5 rounded-full shrink-0">
                              ✓ Retrieved
                            </span>
                          </div>

                          <p className="mt-1.5 line-clamp-3 break-words text-xs leading-relaxed text-muted">
                            {sourceText}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </section>


        {/* =====================================================
            RIGHT PANEL — GENERATED OUTPUT / DELIVERABLE
        ====================================================== */}
        <section className="lg:col-span-4 rounded-2xl border border-border bg-surface p-5 shadow-2xs space-y-4 flex flex-col min-h-[580px]">

          {/* Section Header */}
          <div className="flex items-center justify-between border-b border-border/80 pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-6 w-6 items-center justify-center rounded bg-primary-subtle text-primary border border-primary/20">
                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h2 className="text-xs font-bold uppercase tracking-wider text-foreground">
                  Generated Output
                </h2>
                <p className="text-[11px] text-muted">
                  Local AI generated deliverable
                </p>
              </div>
            </div>

            {output && (
              <button
                onClick={handleDownload}
                className="flex items-center gap-1.5 rounded-lg border border-border bg-surface px-3 py-1.5 text-xs font-medium text-foreground transition hover:bg-background shadow-2xs"
              >
                <svg className="h-3.5 w-3.5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>Download Output</span>
              </button>
            )}
          </div>

          {/* Content Area */}
          <div className="flex-1 flex flex-col justify-start">
            {output ? (
              <div className="space-y-4 flex-1 flex flex-col">

                {/* Validation Status Banner */}
                {validation !== null && (
                  <div
                    className={`rounded-xl border p-3.5 transition-all shadow-2xs ${
                      isValidationFailed
                        ? "border-error/30 bg-error-subtle text-error"
                        : "border-success/30 bg-success-subtle text-success"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2.5">
                        <div
                          className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${
                            isValidationFailed
                              ? "bg-error/20 text-error border border-error/40"
                              : "bg-success/20 text-success border border-success/40"
                          }`}
                        >
                          {isValidationFailed ? "!" : "✓"}
                        </div>

                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-muted">
                            Validation
                          </p>
                          <p
                            className={`mt-0.5 text-xs font-bold ${
                              isValidationFailed ? "text-error" : "text-success"
                            }`}
                          >
                            {isValidationFailed
                              ? "! Output validation failed"
                              : "✓ Output validation passed"}
                          </p>
                        </div>
                      </div>

                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                          isValidationFailed
                            ? "border-error/30 text-error bg-surface"
                            : "border-success/30 text-success bg-surface"
                        }`}
                      >
                        Deterministic
                      </span>
                    </div>

                    {/* Detailed Validation Issues if Failed */}
                    {isValidationFailed && (
                      <div className="mt-2.5 pt-2.5 border-t border-error/20 text-xs text-error space-y-1">
                        {validationIssues.length > 0 ? (
                          <>
                            <p className="font-semibold text-[11px]">Validation details:</p>
                            <ul className="list-disc ml-4 space-y-0.5 text-[11px] leading-relaxed">
                              {validationIssues.map((issue, idx) => (
                                <li key={idx}>{issue}</li>
                              ))}
                            </ul>
                          </>
                        ) : (
                          <p className="text-[11px] leading-relaxed">Output validation failed.</p>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Document Viewer Container */}
                <div className="flex-1 rounded-xl border border-border bg-surface p-4 sm:p-5 shadow-2xs overflow-y-auto max-h-[580px]">
                  <div className="mb-4 border-b border-border pb-3">
                    <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-primary">
                      Sovereign AI Workbench
                    </p>
                    <h3 className="mt-1 text-base font-bold text-foreground">
                      Generated Deliverable
                    </h3>
                    <p className="mt-0.5 text-[11px] text-muted">
                      Generated locally using the confidential document and organizational knowledge base.
                    </p>
                  </div>

                  {/* Markdown Renderer */}
                  <div className="max-w-none text-xs leading-relaxed text-foreground">
                    <ReactMarkdown
                      components={{
                        h1: ({ children }) => (
                          <h1 className="mb-3 mt-4 first:mt-0 border-b border-border pb-2 text-base font-bold text-foreground">
                            {children}
                          </h1>
                        ),
                        h2: ({ children }) => (
                          <h2 className="mb-2 mt-4 text-sm font-semibold uppercase tracking-wide text-primary">
                            {children}
                          </h2>
                        ),
                        h3: ({ children }) => (
                          <h3 className="mb-1.5 mt-3 text-xs font-semibold text-foreground">
                            {children}
                          </h3>
                        ),
                        p: ({ children }) => (
                          <p className="mb-2.5 leading-relaxed text-foreground">
                            {children}
                          </p>
                        ),
                        ul: ({ children }) => (
                          <ul className="mb-3 ml-4 list-disc space-y-1 text-foreground">
                            {children}
                          </ul>
                        ),
                        ol: ({ children }) => (
                          <ol className="mb-3 ml-4 list-decimal space-y-1 text-foreground">
                            {children}
                          </ol>
                        ),
                        li: ({ children }) => (
                          <li className="pl-0.5 leading-relaxed">
                            {children}
                          </li>
                        ),
                        strong: ({ children }) => (
                          <strong className="font-semibold text-foreground">
                            {children}
                          </strong>
                        ),
                        blockquote: ({ children }) => (
                          <blockquote className="my-3 border-l-2 border-primary bg-background px-3 py-2 text-muted italic rounded-r">
                            {children}
                          </blockquote>
                        ),
                        hr: () => (
                          <hr className="my-4 border-border" />
                        ),
                      }}
                    >
                      {output}
                    </ReactMarkdown>
                  </div>
                </div>

              </div>
            ) : (
              <div className="flex flex-1 min-h-[440px] flex-col items-center justify-center text-center p-6 rounded-xl border border-dashed border-border bg-background">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-border bg-surface text-primary shadow-2xs mb-3">
                  <svg
                    className="h-7 w-7 text-primary"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z"
                      stroke="currentColor"
                      strokeWidth="1.6"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M14 2V8H20"
                      stroke="currentColor"
                      strokeWidth="1.6"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M9 13H15M9 17H13"
                      stroke="currentColor"
                      strokeWidth="1.6"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>

                <p className="text-xs font-semibold text-foreground uppercase tracking-wider">
                  Deliverable Console
                </p>

                <p className="mt-1 max-w-xs text-xs leading-relaxed text-muted">
                  Generated approval notes, reports and analysis will appear here.
                </p>
              </div>
            )}
          </div>

        </section>

      </main>

    </div>
  );
}

export default App;