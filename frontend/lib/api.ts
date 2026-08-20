const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";

export interface ResumeUploadResponse {
  filename: string;
  stored_filename: string;
  file_size: number;
  content_type: string;
  status: string;
}

export async function healthCheck() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/health`
  );

  if (!response.ok) {
    throw new Error(
      "Backend health check failed"
    );
  }

  return response.json();
}

export async function uploadResume(
  file: File
): Promise<ResumeUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/v1/resumes/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => null);

    throw new Error(
      error?.detail ??
        "Resume upload failed."
    );
  }

  return response.json();
}


export interface AnalyzeResponse {
  stored_filename: string;

  resume_profile: {
    skills: string[];
    experience: string[];
  };

  job_requirements: {
    skills: string[];
    experience: string[];
    education: string[];
    tools: string[];
    responsibilities: string[];
  };

  matched_skills: string[];
  missing_skills: string[];

  matched_experience: string[];
  unmatched_experience: string[];

  skill_score: number;
  experience_score: number;
  overall_score: number;

  recommendations: string[];
}


export async function analyzeResume(
  storedFilename: string,
  jobDescription: string,
): Promise<AnalyzeResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        stored_filename: storedFilename,
        job_description: jobDescription,
      }),
    },
  );

  if (!response.ok) {
    const error =
      await response.json().catch(
        () => null,
      );

    throw new Error(
      error?.detail ??
        "Resume analysis failed.",
    );
  }

  return response.json();
}