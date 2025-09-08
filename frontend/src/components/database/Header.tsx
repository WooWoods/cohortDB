import UploadButton from "./UploadButton";
import { FilterResponse } from "@/services/api";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  onUploadSuccess: () => void;
}

const Header: React.FC<HeaderProps> = ({ onUploadSuccess }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleLogoutClick = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex items-center justify-end">
      {isAuthenticated && user?.is_admin ? (
        <div className="flex items-center space-x-2">
          <UploadButton onUploadSuccess={onUploadSuccess} />
          <Button onClick={handleLogoutClick}>Log Out</Button>
        </div>
      ) : isAuthenticated ? (
        <Button onClick={handleLogoutClick}>Log Out</Button>
      ) : (
        <Button onClick={handleLoginClick}>Log In</Button>
      )}
    </div>
  );
};

export default Header;
