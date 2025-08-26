import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import UploadButton from "./UploadButton"; // Import the new component

interface HeaderProps {
  onUploadSuccess: () => void;
}

const Header: React.FC<HeaderProps> = ({ onUploadSuccess }) => {
  return (
    <div className="flex items-center justify-between">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input placeholder="Search keywords..." className="pl-8" />
      </div>
      <UploadButton onUploadSuccess={onUploadSuccess} />
    </div>
  );
};

export default Header;
