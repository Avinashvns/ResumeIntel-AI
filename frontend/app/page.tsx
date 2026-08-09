"use client";

import { uploadResume } from "@/lib/api";
import { useState } from "react";

export default function Home() {
  const [resume, setResume] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploading, setUploading] = useState(false);

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
            Analyze your resume against a job description using Agentic RAG
            and MCP-powered AI.
          </p>
        </header>

        {/* Input Section */}
        <section className="grid gap-6 md:grid-cols-2">
          {/* Resume Upload */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">Upload Resume</h2>

            <p className="mt-2 text-sm text-slate-400">
              Upload your resume in PDF format.
            </p>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const file = event.target.files?.[0] ?? null;
                setResume(file);
                setUploadStatus("");
              }}
              className="mt-6 block w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm text-slate-300"
            />

            {resume && (
              <p className="mt-3 text-sm text-slate-400">
                Selected:{" "}
                <span className="text-slate-200">{resume.name}</span>
              </p>
            )}

            <button
              type="button"
              disabled={!resume || uploading}
              onClick={async () => {
                if (!resume) {
                  return;
                }

                try {
                  setUploading(true);
                  setUploadStatus("Uploading...");

                  const result = await uploadResume(resume);

                  setUploadStatus(
                    `Uploaded successfully: ${result.filename}`
                  );
                } catch (error) {
                  setUploadStatus(
                    error instanceof Error
                      ? error.message
                      : "Upload failed"
                  );
                } finally {
                  setUploading(false);
                }
              }}
              className="mt-6 rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {uploading ? "Uploading..." : "Upload Resume"}
            </button>

            {uploadStatus && (
              <p className="mt-4 text-sm text-slate-400">
                {uploadStatus}
              </p>
            )}
          </div>

          {/* Job Description */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold">Job Description</h2>

            <p className="mt-2 text-sm text-slate-400">
              Paste the job description you want to analyze.
            </p>

            <textarea
              placeholder="Paste job description here..."
              className="mt-6 min-h-48 w-full resize-none rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm outline-none placeholder:text-slate-500 focus:border-cyan-500"
            />
          </div>
        </section>

        {/* Analyze Button */}
        <div className="mt-8 text-center">
          <button
            type="button"
            className="rounded-lg bg-cyan-500 px-8 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            Analyze Resume
          </button>
        </div>
      </div>
    </main>
  );
}



// "use client";

// import { useEffect, useState } from "react";
// import { healthCheck } from "@/lib/api";

// export default function Home() {
//   const [status, setStatus] = useState("Checking...");

//   useEffect(() => {
//     healthCheck()
//       .then((data) => {
//         setStatus(data.status);
//       })
//       .catch(() => {
//         setStatus("Backend unavailable");
//       });
//   }, []);

//   return (
//     <main>
//       <h1>ResumeIntel AI</h1>
//       <p>Backend: {status}</p>
//     </main>
//   );
// }