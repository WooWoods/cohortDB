import { toast } from "sonner";

const API_BASE_URL = "http://172.20.8.24:8088/api/v1"; // Assuming backend runs on port 8000

export interface UploadResponse {
  message: string;
}

export interface FilterCriteria {
  filters: {
    [key: string]: [string, number];
  };
}

export interface FilterResponse {
  [tableName: string]: Record<string, unknown>[];
}

export async function uploadData(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE_URL}/data/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to upload file ${file.name}.`);
    }

    return response.json();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : `An unknown error occurred during upload of ${file.name}.`;
    toast.error(`Upload failed: ${errorMessage}`);
    throw error;
  }
}

export async function downloadData(samples: string[]): Promise<Blob> {
  const sampleQuery = samples.join(",");
  try {
    const response = await fetch(`${API_BASE_URL}/data/download?samples=${sampleQuery}`, {
      method: "GET",
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to download data.");
    }

    return response.blob();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during download.";
    toast.error(`Download failed: ${errorMessage}`);
    throw error;
  }
}

export async function filterData(filters: FilterCriteria): Promise<FilterResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/data/filter`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filters),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to filter data.");
    }

    return response.json();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during filter.";
    toast.error(`Filter failed: ${errorMessage}`);
    throw error;
  }
}
