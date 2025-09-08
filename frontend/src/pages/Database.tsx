import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from "@/components/ui/resizable";
import Sidebar from "@/components/database/Sidebar";
import Header from "@/components/database/Header";
import FilteredDataTable from "@/components/database/FilteredDataTable";
import Footer from "@/components/database/Footer";
import { useState, useEffect, useCallback } from "react";
import { FilterResponse, filterData, getInitialData, FilterCriteria, PaginatedFilterResponse } from "@/services/api";
import { useInfiniteQuery } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";

const PAGE_SIZE = 20;

const DatabasePage = () => {
  const [filteredData, setFilteredData] = useState<FilterResponse>({});
  const [totalCount, setTotalCount] = useState(0);
  const [isFiltering, setIsFiltering] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [isFilterActive, setIsFilterActive] = useState(false);

  const { token } = useAuth();

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
    queryFn: async ({ pageParam = 0 }) => {
      if (!token) throw new Error("No token found");
      return getInitialData(pageParam as number, PAGE_SIZE, token)
    },
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
    if (!token) return;
    setIsFiltering(true);
    setIsSearching(false);
    if (Object.keys(filters.filters).length > 0) {
      setIsFilterActive(true);
      const data = await filterData(filters, token);
      setFilteredData(data);
      setTotalCount(Object.values(data).flat().length);
    } else {
      setIsFilterActive(false);
      refetch();
    }
    setIsFiltering(false);
  };

  const handleUploadSuccess = () => {
    refetch(); // Refetch all data after upload
  };

  const handleSearch = async (data: FilterResponse) => {
    setIsFiltering(true);
    setIsSearching(true);
    setFilteredData(data);
    setTotalCount(Object.values(data).flat().length);
    setIsFiltering(false);
  };

  const handleClearSearch = () => {
    setIsSearching(false);
    refetch();
  };

  const handleClearFilter = () => {
    setIsFilterActive(false);
    refetch();
  };

  const handleScroll = useCallback((event: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = event.currentTarget;
    if (scrollHeight - scrollTop - clientHeight < 50 && hasNextPage && !isFetchingNextPage && !isFiltering && !isSearching && !isFilterActive) {
      fetchNextPage();
    }
  }, [fetchNextPage, hasNextPage, isFetchingNextPage, isFiltering, isSearching, isFilterActive]);

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
          <Sidebar onFilterApply={handleFilterApply} onSearch={handleSearch} onClearSearch={handleClearSearch} onClearFilter={handleClearFilter} />
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize={75}>
          <div className="flex flex-col h-full p-4 space-y-4">
            <Header onUploadSuccess={handleUploadSuccess} />
            <div className="flex-grow overflow-auto">
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
                  <FilteredDataTable data={filteredData} onScroll={handleScroll} />
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
