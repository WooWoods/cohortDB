import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import Sidebar from "@/components/database/Sidebar";
import Header from "@/components/database/Header";
import FilteredDataTable from "@/components/database/FilteredDataTable"; // Import the new component
import Footer from "@/components/database/Footer";
import { useState, useEffect, useRef, useCallback } from "react";
import { FilterResponse, filterData, getInitialData, FilterCriteria, PaginatedFilterResponse } from "@/services/api";
import { useInfiniteQuery } from "@tanstack/react-query";

const PAGE_SIZE = 20;

const DatabasePage = () => {
  const [filteredData, setFilteredData] = useState<FilterResponse>({});
  const [totalCount, setTotalCount] = useState(0);
  const [isFiltering, setIsFiltering] = useState(false); // To manage filter state
  const scrollRef = useRef<HTMLDivElement>(null);

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
    error,
    refetch,
  } = useInfiniteQuery<PaginatedFilterResponse, Error>({
    queryKey: ["cohortData"],
    queryFn: async ({ pageParam = 0 }) => getInitialData(pageParam as number, PAGE_SIZE),
    getNextPageParam: (lastPage, allPages) => {
      const loadedCount = allPages.reduce((acc, page) => {
        const tableNames = Object.keys(page.data);
        if (tableNames.length > 0) {
          return acc + page.data[tableNames[0]].length;
        }
        return acc;
      }, 0);
      return loadedCount < lastPage.total_count ? allPages.length * PAGE_SIZE : undefined;
    },
    initialPageParam: 0,
  });

  useEffect(() => {
    if (data) {
      const combinedData: FilterResponse = {};
      let currentTotalCount = 0;

      data.pages.forEach((page) => {
        currentTotalCount = page.total_count;
        for (const tableName in page.data) {
          if (Object.prototype.hasOwnProperty.call(page.data, tableName)) {
            if (!combinedData[tableName]) {
              combinedData[tableName] = [];
            }
            combinedData[tableName].push(...page.data[tableName]);
          }
        }
      });
      setFilteredData(combinedData);
      setTotalCount(currentTotalCount);
    }
  }, [data]);

  useEffect(() => {
    if (isError) {
      console.error("Initial data fetch failed:", error);
    }
  }, [isError, error]);

  const handleFilterApply = async (filters: FilterCriteria) => {
    setIsFiltering(true);
    if (Object.keys(filters.filters).length > 0) {
      const data = await filterData(filters);
      setFilteredData(data);
      setTotalCount(Object.values(data).flat().length); // Assuming filterData returns all matching records
    } else {
      // If filters are cleared, refetch initial data
      refetch();
    }
    setIsFiltering(false);
  };

  const handleUploadSuccess = () => {
    refetch(); // Refetch all data after upload
  };

  const handleSearch = async (data: FilterResponse) => {
    setIsFiltering(true);
    setFilteredData(data);
    setTotalCount(Object.values(data).flat().length); // Assuming searchData returns all matching records
    setIsFiltering(false);
  };

  const handleScroll = useCallback(() => {
    const { current } = scrollRef;
    if (current && !isFetchingNextPage && hasNextPage && !isFiltering) {
      const { scrollTop, scrollHeight, clientHeight } = current;
      if (scrollHeight - scrollTop - clientHeight < 50) { // 50px from bottom
        fetchNextPage();
      }
    }
  }, [fetchNextPage, isFetchingNextPage, hasNextPage, isFiltering]);

  useEffect(() => {
    const { current } = scrollRef;
    if (current) {
      current.addEventListener("scroll", handleScroll);
      return () => current.removeEventListener("scroll", handleScroll);
    }
  }, [handleScroll]);

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
            <div className="flex-grow overflow-auto" ref={scrollRef}>
              {isLoading && !isFetchingNextPage ? (
                <div className="flex items-center justify-center h-full text-muted-foreground">
                  Loading data...
                </div>
              ) : isError ? (
                <div className="flex items-center justify-center h-full text-destructive">
                  Error loading data.
                </div>
              ) : (
                <>
                  <FilteredDataTable data={filteredData} />
                  {isFetchingNextPage && (
                    <div className="flex items-center justify-center p-4 text-muted-foreground">
                      Loading more data...
                    </div>
                  )}
                  {!hasNextPage && !isLoading && !isFiltering && (
                    <div className="flex items-center justify-center p-4 text-muted-foreground">
                      No more data to load.
                    </div>
                  )}
                </>
              )}
            </div>
            <Footer filteredData={filteredData} totalCount={totalCount} />
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
};

export default DatabasePage;
