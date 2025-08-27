import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { downloadData, FilterResponse } from "@/services/api";
import { toast } from "sonner";
import { useMutation } from "@tanstack/react-query";

interface FooterProps {
  filteredData: FilterResponse;
  totalCount: number;
}

const Footer: React.FC<FooterProps> = ({ filteredData, totalCount }) => {
  const downloadMutation = useMutation({
    mutationFn: (samples: string[]) => downloadData(samples),
    onSuccess: (blob) => {
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "cohort_data.xlsx");
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      toast.success("Data downloaded successfully!");
    },
    onError: (error) => {
      toast.error(`Download failed: ${error.message}`);
    },
  });

  const handleDownloadClick = () => {
    const allSamples: string[] = [];
    for (const tableName in filteredData) {
      if (Object.prototype.hasOwnProperty.call(filteredData, tableName)) {
        const records = filteredData[tableName];
        records.forEach((record) => {
          if (record.sample && typeof record.sample === "string") {
            allSamples.push(record.sample);
          }
        });
      }
    }
    
    // Remove duplicates and trigger download
    const uniqueSamples = Array.from(new Set(allSamples));
    if (uniqueSamples.length > 0) {
      downloadMutation.mutate(uniqueSamples);
    } else {
      toast.info("No samples to download.");
    }
  };

  return (
    <div className="flex justify-between items-center">
      <div className="text-sm text-muted-foreground">
        Total entries: {totalCount}
      </div>
      <Button onClick={handleDownloadClick} disabled={downloadMutation.isPending}>
        <Download className="mr-2 h-4 w-4" />
        {downloadMutation.isPending ? "Exporting..." : "Export Data"}
      </Button>
    </div>
  );
};

export default Footer;
