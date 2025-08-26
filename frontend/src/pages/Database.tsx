import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import Sidebar from "@/components/database/Sidebar";
import Header from "@/components/database/Header";
import FilteredDataTable from "@/components/database/FilteredDataTable"; // Import the new component
import Footer from "@/components/database/Footer";
import { useState, useEffect } from "react";
import { FilterResponse, filterData, getInitialData, FilterCriteria } from "@/services/api";
import { useQuery } from "@tanstack/react-query";

const DatabasePage = () => {
  const [filteredData, setFilteredData] = useState<FilterResponse>({});
  const [refreshTrigger, setRefreshTrigger] = useState(0); // To manually trigger data refresh

  // Initial data fetch or refresh after upload/filter
  const { data, isLoading, isError, refetch, error } = useQuery({
    queryKey: ["cohortData", refreshTrigger],
    queryFn: () => getInitialData(), // Fetch initial data
  });

  useEffect(() => {
    if (data) {
      setFilteredData(data);
    }
  }, [data]);

  useEffect(() => {
    if (isError) {
      console.error("Initial data fetch failed:", error);
      // toast.error("Failed to load initial data."); // Toast handled by api.ts
    }
  }, [isError, error]);

  useEffect(() => {
    refetch();
  }, [refreshTrigger]); // Only refetch when refreshTrigger changes

  const handleFilterApply = async (filters: FilterCriteria) => {
    if (Object.keys(filters.filters).length > 0) {
      const data = await filterData(filters);
      setFilteredData(data);
    } else {
      // If filters are cleared, refetch initial data
      const data = await getInitialData();
      setFilteredData(data);
    }
  };

  const handleUploadSuccess = () => {
    setRefreshTrigger((prev) => prev + 1); // Increment to trigger refetch
  };

  const handleSearch = (data: FilterResponse) => {
    setFilteredData(data);
  };

  return (
    <div className="h-screen w-screen">
      <ResizablePanelGroup
        direction="horizontal"
        className="h-full w-full"
      >
        <ResizablePanel
          defaultSize={25}
          minSize={20}
          maxSize={35}
          collapsible={true}
          collapsedSize={0}
        >
          <Sidebar onFilterApply={handleFilterApply} />
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize={75}>
          <div className="flex flex-col h-full p-4 space-y-4">
            <Header onUploadSuccess={handleUploadSuccess} onSearch={handleSearch} />
            <div className="flex-grow overflow-auto">
              {isLoading ? (
                <div className="flex items-center justify-center h-full text-muted-foreground">
                  Loading data...
                </div>
              ) : isError ? (
                <div className="flex items-center justify-center h-full text-destructive">
                  Error loading data.
                </div>
              ) : (
                <FilteredDataTable data={filteredData} />
              )}
            </div>
            <Footer filteredData={filteredData} />
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
};

export default DatabasePage;
