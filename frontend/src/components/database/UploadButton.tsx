import React, { useRef } from "react";
import { Button } from "@/components/ui/button";
import { Upload } from "lucide-react";
import { uploadData } from "@/services/api";
import { toast } from "sonner";
import { useMutation } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext"; // Import useAuth

interface UploadButtonProps {
  onUploadSuccess: () => void;
}

const UploadButton: React.FC<UploadButtonProps> = ({ onUploadSuccess }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { isAuthenticated, token } = useAuth(); // Get isAuthenticated and token from AuthContext

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      if (!token) {
        throw new Error("No authentication token found. Please log in.");
      }
      return uploadData(file, token); // Pass token to uploadData
    },
    onSuccess: (data) => {
      toast.success(data.message || "File uploaded successfully!");
      onUploadSuccess();
      if (fileInputRef.current) fileInputRef.current.value = "";
    },
    onError: (error) => {
      toast.error(`Upload failed: ${error.message}`);
    },
  });

  const handleUploadClick = () => {
    if (!isAuthenticated) {
      toast.error("You must be logged in to upload data.");
      return;
    }
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      uploadMutation.mutate(file);
    }
  };

  return (
    <div>
      <input
        type="file"
        id="file-input"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
        accept=".csv,.xlsx"
      />
      <Button onClick={handleUploadClick} disabled={uploadMutation.isPending || !isAuthenticated}>
        <Upload className="mr-2 h-4 w-4" />
        {uploadMutation.isPending ? "Uploading..." : "Upload Data"}
      </Button>
    </div>
  );
};

export default UploadButton;
