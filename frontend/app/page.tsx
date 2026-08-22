"use client";

import { useState } from "react";

import {
  analyzeResume,
  uploadResume,
  type AnalyzeResponse,
  type ResumeUploadResponse,
} from "@/lib/api";

const MAX_FILE_SIZE =
  5 * 1024 * 1024;

export default function Home() {
  const [resume, setResume] =
    useState<File | null>(null);

  const [storedFilename, setStoredFilename] =
    useState("");

  const [uploading, setUploading] =
    useState(false);

  const [uploadResult, setUploadResult] =
    useState<ResumeUploadResponse | null>(
      null,
    );

  const [jobDescription, setJobDescription] =
    useState("");

  const [analyzing, setAnalyzing] =
    useState(false);

  const [analysisResult, setAnalysisResult] =
    useState<AnalyzeResponse | null>(null);

  const [error, setError] =
    useState("");

  function ScoreCard({
    title,
    score,
  }: {
    title: string;
    score: number;
  }) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-950 p-5">
        <p className="text-sm text-slate-400">
          {title}
        </p>

        <p className="mt-2 text-3xl font-bold text-white">
          {score.toFixed(0)}%
        </p>

        <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full rounded-full bg-cyan-500 transition-all"
            style={{
              width: `${Math.min(
                Math.max(score, 0),
                100,
              )}%`,
            }}
          />
        </div>
      </div>
    );
  }


  function ResultList({
    title,
    items,
    emptyMessage,
    variant,
  }: {
    title: string;
    items: string[];
    emptyMessage: string;
    variant: "success" | "danger";
  }) {
    const icon =
      variant === "success"
        ? "✓"
        : "✗";

    const iconClass =
      variant === "success"
        ? "text-emerald-400"
        : "text-red-400";

    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h3 className="text-lg font-semibold">
          {title}
        </h3>

        {items.length === 0 ? (
          <p className="mt-4 text-sm text-slate-500">
            {emptyMessage}
          </p>
        ) : (
          <ul className="mt-4 space-y-2">
            {items.map((item, index) => (
              <li
                key={`${item}-${index}`}
                className="flex items-start gap-3 rounded-lg bg-slate-950 p-3 text-sm text-slate-300"
              >
                <span
                  className={`font-bold ${iconClass}`}
                >
                  {icon}
                </span>

                <span>{item}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  }

  const validateFile = (
    file: File,
  ): string | null => {
    if (
      file.type !== "application/pdf"
    ) {
      return "Only PDF files are allowed.";
    }

    if (
      file.size > MAX_FILE_SIZE
    ) {
      return (
        "Resume file must be smaller than 5 MB."
      );
    }

    if (file.size === 0) {
      return "Resume file cannot be empty.";
    }

    return null;
  };

  const handleFile = (
    file: File,
  ) => {
    setError("");
    setUploadResult(null);
    setStoredFilename("");
    setAnalysisResult(null);

    const validationError =
      validateFile(file);

    if (validationError) {
      setResume(null);
      setError(validationError);
      return;
    }

    setResume(file);
  };

  const handleUpload = async () => {
    if (!resume || uploading || analyzing) {
      return;
    }

    setUploading(true);
    setError("");
    setUploadResult(null);
    setStoredFilename("");
    setAnalysisResult(null);

    try {
      const result =
        await uploadResume(resume);

      setUploadResult(result);

      setStoredFilename(
        result.stored_filename,
      );
    } catch (error) {
      setUploadResult(null);
      setStoredFilename("");

      setError(
        error instanceof Error
          ? error.message
          : "Resume upload failed.",
      );
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (uploading || analyzing) {
      return;
    }

    setError("");
    setAnalysisResult(null);

    if (!storedFilename) {
      setError(
        "Please upload your resume first.",
      );

      return;
    }

    if (!jobDescription.trim()) {
      setError(
        "Please enter a job description.",
      );

      return;
    }

    setAnalyzing(true);

    try {
      const result =
        await analyzeResume(
          storedFilename,
          jobDescription.trim(),
        );

      setAnalysisResult(result);
    } catch (error) {
      setAnalysisResult(null);

      setError(
        error instanceof Error
          ? error.message
          : "Resume analysis failed.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  const canAnalyze =
    Boolean(storedFilename) &&
    Boolean(jobDescription.trim()) &&
    !uploading &&
    !analyzing;

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Header */}

        <header className="mb-12 text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-cyan-400">
            AI-Powered Career Intelligence
          </p>

          <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
            ResumeIntel AI
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-slate-400">
            Analyze your resume against a
            job description using Agentic RAG
            and MCP-powered AI.
          </p>
        </header>

        {/* Resume + JD */}

        <section className="grid gap-6 md:grid-cols-2">

          {/* Resume Upload */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">
              Upload Resume
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Upload your resume in PDF format.
            </p>

            <label
              htmlFor="resume-upload"
              className="mt-6 flex min-h-48 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 px-6 text-center transition hover:border-cyan-500"
            >
              <span className="text-4xl">
                📄
              </span>

              <span className="mt-4 text-sm font-medium text-slate-200">
                Choose a PDF resume
              </span>

              <span className="mt-2 text-xs text-slate-500">
                PDF only • Maximum 5 MB
              </span>

              <input
                id="resume-upload"
                type="file"
                accept=".pdf,application/pdf"
                className="hidden"
                disabled={
                  uploading ||
                  analyzing
                }
                onChange={(event) => {
                  const file =
                    event.target.files?.[0];

                  if (file) {
                    handleFile(file);
                  }
                }}
              />
            </label>

            {resume && (
              <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4">
                <p className="text-sm font-medium text-slate-200">
                  Selected Resume
                </p>

                <p className="mt-1 truncate text-sm text-slate-400">
                  {resume.name}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {(
                    resume.size /
                    1024 /
                    1024
                  ).toFixed(2)}{" "}
                  MB
                </p>
              </div>
            )}

            <button
              type="button"
              disabled={
                !resume ||
                uploading ||
                analyzing
              }
              onClick={handleUpload}
              className="mt-6 w-full rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {uploading
                ? "Uploading..."
                : "Upload Resume"}
            </button>

            {uploadResult && (
              <div className="mt-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
                <p className="text-sm font-semibold text-emerald-400">
                  Resume uploaded successfully
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  {uploadResult.filename}
                </p>

                <p className="mt-1 break-all text-xs text-slate-500">
                  Document ID:{" "}
                  {uploadResult.stored_filename}
                </p>
              </div>
            )}
          </div>

          {/* Job Description */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">
              Job Description
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Paste the job description you
              want to analyze.
            </p>

            <textarea
              value={jobDescription}
              onChange={(event) => {
                setJobDescription(
                  event.target.value,
                );

                setError("");
                setAnalysisResult(null);
              }}
              placeholder="Paste job description here..."
              disabled={
                uploading ||
                analyzing
              }
              className="mt-6 min-h-48 w-full resize-none rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm text-slate-200 outline-none placeholder:text-slate-500 focus:border-cyan-500 disabled:cursor-not-allowed disabled:opacity-50"
            />

            <div className="mt-2 flex items-center justify-between">
              <p className="text-xs text-slate-500">
                {jobDescription.length}{" "}
                characters
              </p>

              <button
                type="button"
                onClick={() => {
                  setJobDescription("");
                  setAnalysisResult(null);
                  setError("");
                }}
                disabled={
                  !jobDescription ||
                  analyzing
                }
                className="text-xs text-slate-500 transition hover:text-slate-300 disabled:cursor-not-allowed disabled:opacity-30"
              >
                Clear
              </button>
            </div>
          </div>
        </section>

        {/* Analyze */}

        <div className="mt-8 text-center">
          <button
            type="button"
            disabled={!canAnalyze}
            onClick={handleAnalyze}
            className="rounded-lg bg-cyan-500 px-8 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-500"
          >
            {analyzing ? (
              <span className="inline-flex items-center gap-2">
                <span
                  aria-hidden="true"
                  className="h-4 w-4 animate-spin rounded-full border-2 border-slate-950/30 border-t-slate-950"
                />
                Analyzing...
              </span>
            ) : (
              "Analyze Resume"
            )}
          </button>

          <p className="mt-2 text-xs text-slate-600">
            Upload a resume and enter a job
            description to start analysis.
          </p>
        </div>

        {/* Error */}

        {error && (
          <div
            role="alert"
            className="mx-auto mt-6 max-w-2xl rounded-xl border border-red-500/30 bg-red-500/10 p-4"
          >
            <div className="flex items-start gap-3">
              <span className="font-bold text-red-400">
                ✕
              </span>

              <div>
                <p className="text-sm font-semibold text-red-400">
                  Something went wrong
                </p>

                <p className="mt-1 text-sm text-red-300/80">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Results Dashboard */}

        {analysisResult && (
          <section className="mt-12">
            <div className="mb-6">
              <p className="text-sm font-semibold uppercase tracking-widest text-cyan-400">
                Analysis Results
              </p>

              <h2 className="mt-2 text-3xl font-bold">
                Resume Match Dashboard
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Analysis generated from your resume and
                the provided job description.
              </p>
            </div>

            {/* Score Cards */}

            <div className="grid gap-4 md:grid-cols-3">
              <ScoreCard
                title="Overall Match"
                score={
                  analysisResult.overall_score
                }
              />

              <ScoreCard
                title="Skill Match"
                score={
                  analysisResult.skill_score
                }
              />

              <ScoreCard
                title="Experience Match"
                score={
                  analysisResult.experience_score
                }
              />
            </div>

            {/* Skills */}

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <ResultList
                title="Matched Skills"
                items={
                  analysisResult.matched_skills
                }
                emptyMessage="No matching skills found."
                variant="success"
              />

              <ResultList
                title="Missing Skills"
                items={
                  analysisResult.missing_skills
                }
                emptyMessage="No missing skills detected."
                variant="danger"
              />
            </div>

            {/* Experience */}

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <ResultList
                title="Matched Experience"
                items={
                  analysisResult.matched_experience
                }
                emptyMessage="No matched experience requirements."
                variant="success"
              />

              <ResultList
                title="Unmatched Experience"
                items={
                  analysisResult.unmatched_experience
                }
                emptyMessage="All experience requirements matched."
                variant="danger"
              />
            </div>

            {/* Agent Activity */}

            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">
                    Agent Activity
                  </h3>

                  <p className="mt-1 text-sm text-slate-400">
                    Analysis pipeline execution stages.
                  </p>
                </div>

                <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400">
                  Completed
                </span>
              </div>

              <div className="mt-5 space-y-3">
                {analysisResult.activity.map(
                  (activity, index) => (
                    <div
                      key={`${activity.stage}-${index}`}
                      className="flex items-center gap-4 rounded-xl border border-slate-800 bg-slate-950 p-4"
                    >
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500/10">
                        <span className="text-sm font-bold text-emerald-400">
                          {activity.status ===
                            "completed"
                            ? "✓"
                            : "•"}
                        </span>
                      </div>

                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-slate-200">
                          {activity.stage}
                        </p>

                        <p className="mt-1 text-xs capitalize text-slate-500">
                          {activity.status}
                        </p>
                      </div>
                    </div>
                  ),
                )}
              </div>
            </div>

            {/* Recommendations */}

            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-lg font-semibold">
                Recommendations
              </h3>

              {analysisResult.recommendations.length ===
                0 ? (
                <p className="mt-4 text-sm text-slate-500">
                  No recommendations available.
                </p>
              ) : (
                <ul className="mt-4 space-y-3">
                  {analysisResult.recommendations.map(
                    (recommendation, index) => (
                      <li
                        key={`${recommendation}-${index}`}
                        className="flex gap-3 rounded-lg bg-slate-950 p-4 text-sm text-slate-300"
                      >
                        <span className="font-semibold text-cyan-400">
                          {index + 1}.
                        </span>

                        <span>
                          {recommendation}
                        </span>
                      </li>
                    ),
                  )}
                </ul>
              )}
            </div>

            {/* Resume Profile */}

            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-lg font-semibold">
                Resume Profile
              </h3>

              <p className="mt-2 text-sm text-slate-400">
                Extracted skills from your resume.
              </p>

              <div className="mt-4 flex flex-wrap gap-2">
                {analysisResult.resume_profile.skills
                  .length === 0 ? (
                  <p className="text-sm text-slate-500">
                    No skills extracted.
                  </p>
                ) : (
                  analysisResult.resume_profile.skills.map(
                    (skill, index) => (
                      <span
                        key={`${skill}-${index}`}
                        className="rounded-full border border-slate-700 bg-slate-950 px-3 py-1 text-xs text-slate-300"
                      >
                        {skill}
                      </span>
                    ),
                  )
                )}
              </div>
            </div>

            {/* Job Requirements */}

            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-lg font-semibold">
                Job Requirements
              </h3>

              <p className="mt-2 text-sm text-slate-400">
                Requirements extracted from the job
                description.
              </p>

              <div className="mt-4 flex flex-wrap gap-2">
                {[
                  ...analysisResult.job_requirements.skills,
                  ...analysisResult.job_requirements.tools,
                ].length === 0 ? (
                  <p className="text-sm text-slate-500">
                    No technical requirements extracted.
                  </p>
                ) : (
                  [
                    ...analysisResult.job_requirements.skills,
                    ...analysisResult.job_requirements.tools,
                  ].map((requirement, index) => (
                    <span
                      key={`${requirement}-${index}`}
                      className="rounded-full border border-slate-700 bg-slate-950 px-3 py-1 text-xs text-slate-300"
                    >
                      {requirement}
                    </span>
                  ))
                )}
              </div>
            </div>
          </section>
        )}


      </div>
    </main>
  );
}