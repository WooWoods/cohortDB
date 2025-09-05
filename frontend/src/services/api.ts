import { toast } from "sonner";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8088/api/v1";

export interface UploadResponse {
  message: string;
}

export interface FilterCriteria {
  filters: {
    [key: string]: [string, number];
  };
}

export interface PaginatedFilterResponse {
  data: {
    [tableName: string]: Record<string, unknown>[];
  };
  total_count: number;
}

export interface FilterResponse {
  [tableName: string]: Record<string, unknown>[];
}

export interface User {
  id: number;
  username: string;
  is_admin: boolean;
  created_at: string;
}

export async function uploadData(file: File, token: string): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  console.log("DEBUG (Frontend): Token being sent for upload:", token); // Add this line
  try {
    const response = await fetch(`${API_BASE_URL}/data/upload`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
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

export async function getInitialData(offset: number = 0, limit: number = 20): Promise<PaginatedFilterResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/data/initial?offset=${offset}&limit=${limit}`, {
      method: "GET",
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch initial data.");
    }

    return response.json();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during initial data fetch.";
    toast.error(`Initial data fetch failed: ${errorMessage}`);
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

export async function searchData(searchTerm: string): Promise<FilterResponse> {
  const formData = new FormData();
  formData.append("search_term", searchTerm);

  try {
    const response = await fetch(`${API_BASE_URL}/data/search`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to search data.");
    }

    return response.json();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during search.";
    toast.error(`Search failed: ${errorMessage}`);
    throw error;
  }
}

export async function loginUser(username: string, password: string): Promise<string> {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  try {
    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed.");
    }

    const data = await response.json();
    return data.access_token;
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred during login.";
    toast.error(`Login failed: ${errorMessage}`);
    throw error;
  }
}

export function logoutUser(): void {
  localStorage.removeItem('access_token');
}

export async function getMe(token: string): Promise<User> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch user data.");
    }

    return response.json();
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred while fetching user data.";
    toast.error(`Failed to get user data: ${errorMessage}`);
    throw error;
  }
}
