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
    if (!resume) {
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
            {analyzing
              ? "Analyzing..."
              : "Analyze Resume"}
          </button>

          <p className="mt-2 text-xs text-slate-600">
            Upload a resume and enter a job
            description to start analysis.
          </p>
        </div>

        {/* Error */}

        {error && (
          <div className="mx-auto mt-6 max-w-2xl rounded-xl border border-red-500/30 bg-red-500/10 p-4">
            <p className="text-center text-sm text-red-400">
              {error}
            </p>
          </div>
        )}

        {/* Temporary Feature 39 Result */}

        {analysisResult && (
          <section className="mx-auto mt-10 max-w-4xl rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">
              Analysis Complete
            </h2>

            <div className="mt-6 grid gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-slate-950 p-4 text-center">
                <p className="text-xs text-slate-500">
                  Overall Match
                </p>

                <p className="mt-2 text-3xl font-bold text-cyan-400">
                  {analysisResult.overall_score}%
                </p>
              </div>

              <div className="rounded-xl bg-slate-950 p-4 text-center">
                <p className="text-xs text-slate-500">
                  Skill Match
                </p>

                <p className="mt-2 text-3xl font-bold text-emerald-400">
                  {analysisResult.skill_score}%
                </p>
              </div>

              <div className="rounded-xl bg-slate-950 p-4 text-center">
                <p className="text-xs text-slate-500">
                  Experience Match
                </p>

                <p className="mt-2 text-3xl font-bold text-purple-400">
                  {analysisResult.experience_score}%
                </p>
              </div>
            </div>

            <div className="mt-6">
              <p className="text-sm font-semibold">
                Matched Skills
              </p>

              <p className="mt-2 text-sm text-slate-400">
                {analysisResult.matched_skills
                  .length > 0
                  ? analysisResult.matched_skills.join(
                      ", ",
                    )
                  : "None"}
              </p>
            </div>

            <div className="mt-6">
              <p className="text-sm font-semibold">
                Missing Skills
              </p>

              <p className="mt-2 text-sm text-slate-400">
                {analysisResult.missing_skills
                  .length > 0
                  ? analysisResult.missing_skills.join(
                      ", ",
                    )
                  : "None"}
              </p>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}