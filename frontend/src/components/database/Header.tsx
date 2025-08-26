import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import UploadButton from "./UploadButton";
import { searchData, FilterResponse } from "@/services/api";
import { useState } from "react";

interface HeaderProps {
  onUploadSuccess: () => void;
  onSearch: (data: FilterResponse) => void;
}

const Header: React.FC<HeaderProps> = ({ onUploadSuccess, onSearch }) => {
  const [searchQuery, setSearchQuery] = useState<string>("");

  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();
    if (searchQuery.trim()) {
      try {
        const result = await searchData(searchQuery);
        onSearch(result);
      } catch (error) {
        console.error("Search failed:", error);
      }
    }
  };

  return (
    <div className="flex items-center justify-between">
      <form onSubmit={handleSearch} className="relative w-full max-w-sm">
        <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search sample names (e.g., MO026 or prefix: MO*)"
          className="pl-8"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </form>
      <UploadButton onUploadSuccess={onUploadSuccess} />
    </div>
  );
};

export default Header;
