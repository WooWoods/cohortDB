import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { MadeWithDyad } from "@/components/made-with-dyad";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="text-center p-8">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-800 dark:text-gray-100">
          Internal Database UI
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          A sample application to browse and filter internal data.
        </p>
        <Link to="/database">
          <Button size="lg">Go to Database</Button>
        </Link>
      </div>
      <div className="absolute bottom-4">
        <MadeWithDyad />
      </div>
    </div>
  );
};

export default Index;