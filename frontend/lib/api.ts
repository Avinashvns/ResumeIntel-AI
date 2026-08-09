const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";

export async function healthCheck() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/health`
  );

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}



export async function uploadResume(file: File) {
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
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail ?? "Resume upload failed"
    );
  }

  return response.json();
}