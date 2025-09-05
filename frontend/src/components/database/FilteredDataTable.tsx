import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { FilterResponse } from "@/services/api";

interface FilteredDataTableProps {
  data: FilterResponse;
}

const DESIRED_COLUMNS = [
  "sample",
  "ptid",
  "gender",
  "age",
  "lambda_dna_conversion_rate",
  "mean_insert_size",
  "percent_duplication",
  "pct_selected_bases",
  "fold_80_base_penalty",
  "pct_target_bases_10x",
];

const processData = (data: FilterResponse) => {
  const combinedRecords: Record<string, unknown>[] = [];
  const sampleMap: Map<string, Record<string, unknown>> = new Map();

  // Iterate through each table and its records
  for (const tableName in data) {
    if (Object.prototype.hasOwnProperty.call(data, tableName)) {
      const records = data[tableName];
      records.forEach((record) => {
        const sample = record.sample as string;
        if (sample) {
          if (!sampleMap.has(sample)) {
            sampleMap.set(sample, { sample }); // Initialize with sample ID
          }
          // Merge current record's properties into the existing sample entry
          sampleMap.set(sample, { ...sampleMap.get(sample), ...record });
        }
      });
    }
  }

  // Filter and order columns based on DESIRED_COLUMNS
  sampleMap.forEach((record) => {
    const newRecord: Record<string, unknown> = {};
    DESIRED_COLUMNS.forEach((col) => {
      newRecord[col] = record[col] !== undefined ? record[col] : "N/A";
    });
    combinedRecords.push(newRecord);
  });

  return combinedRecords;
};

const FilteredDataTable: React.FC<FilteredDataTableProps> = ({ data }) => {
  const processedData = processData(data);

  if (processedData.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        No data to display. Apply filters or upload data.
      </div>
    );
  }

  return (
    <div className="p-4">
      <h3 className="text-lg font-semibold mb-4">Combined Cohort Data</h3>
      <Table
        className="border-separate border-spacing-0 w-full"
        maxHeight="480px"
        showBorder
      >
        <TableHeader>
          <TableRow>
            {DESIRED_COLUMNS.map((key, index) => (
                <TableHead
                  key={key}
                  className={`sticky top-0 bg-white dark:bg-gray-950 ${
                    index === 0 ? "left-0 z-30" : "z-20"
                  }`}
                >
                  {key}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>

          <TableBody>
            {processedData.map((record, r) => (
              <TableRow key={r}>
                {DESIRED_COLUMNS.map((col, c) => (
                  <TableCell
                    key={c}
                    className={
                      c === 0
                        ? "sticky left-0 bg-white dark:bg-gray-950 z-10"
                        : ""
                    }
                  >
                    {String(record[col])}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
  );
};

export default FilteredDataTable;
