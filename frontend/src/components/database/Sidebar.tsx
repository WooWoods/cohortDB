import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PlusCircle, X } from "lucide-react";
import { filterData, FilterCriteria, FilterResponse } from "@/services/api";
import { toast } from "sonner";
import { useMutation } from "@tanstack/react-query";

type Filter = {
  id: number;
  field: string;
  operator: string;
  value: string;
};

interface SidebarProps {
  onFilterApply: (filters: FilterCriteria) => void;
}

const FILTERABLE_COLUMNS = {
  "age": "Age",
  "total_bases": "Total Bases",
  "puc19vector": "pUC19 Vector",
  "lambda_dna_conversion_rate": "Lambda DNA Conversion Rate",
  "human": "Human",
  "lambda_dna": "Lambda DNA",
  "pUC19": "pUC19",
  "q30_rate": "Q30 Rate",
  "mean_insert_size": "Mean Insert Size",
  "percent_duplication": "Percent Duplication",
  "pct_selected_bases": "Pct Selected Bases",
  "fold_enrichment": "Fold Enrichment",
  "zero_cvg_targets_pct": "Zero Cvg Targets Pct",
  "mean_target_coverage": "Mean Target Coverage",
  "pct_exc_dupe": "Pct Exc Dupe",
  "pct_exc_off_target": "Pct Exc Off Target",
  "fold_80_base_penalty": "Fold 80 Base Penalty",
  "pct_target_bases_10x": "Pct Target Bases 10x",
  "pct_target_bases_20x": "Pct Target Bases 20x",
  "pct_target_bases_30x": "Pct Target Bases 30x",
};

const Sidebar: React.FC<SidebarProps> = ({ onFilterApply }) => {
  const [filters, setFilters] = useState<Filter[]>([]);

  const filterMutation = useMutation({
    mutationFn: (criteria: FilterCriteria) => filterData(criteria),
    onSuccess: () => {
      toast.success("Data filtered successfully!");
      // The actual data update will be handled by DatabasePage based on the filters passed
    },
    onError: (error) => {
      toast.error(`Filter failed: ${error.message}`);
    },
  });

  const addFilter = () => {
    setFilters([...filters, { id: Date.now(), field: "age", operator: ">=", value: "" }]);
  };

  const removeFilter = (id: number) => {
    setFilters(filters.filter((filter) => filter.id !== id));
  };

  const updateFilter = (id: number, newFilter: Partial<Filter>) => {
    setFilters(
      filters.map((filter) => (filter.id === id ? { ...filter, ...newFilter } : filter))
    );
  };

  const applyFilters = () => {
    const criteria: FilterCriteria = {
      filters: {},
    };

    filters.forEach((filter) => {
      let parsedValue: number | string = filter.value;
      // Attempt to parse value as number if field is numeric
      if (Object.keys(FILTERABLE_COLUMNS).includes(filter.field)) {
        parsedValue = parseFloat(filter.value);
        if (isNaN(parsedValue)) {
          toast.error(`Invalid number for ${FILTERABLE_COLUMNS[filter.field as keyof typeof FILTERABLE_COLUMNS]}.`);
          return; // Skip this filter if value is not a valid number
        }
      }
      criteria.filters[filter.field] = [filter.operator, parsedValue as number];
    });

    if (Object.keys(criteria.filters).length > 0) {
      filterMutation.mutate(criteria);
      onFilterApply(criteria); // Pass the criteria to the parent
    } else {
      toast.info("No filters applied. Displaying initial data.");
      onFilterApply({ filters: {} }); // Pass empty filters to trigger initial data load
    }
  };

  const operatorMap: { [key: string]: string } = {
    "equals": "==",
    "greaterThan": ">",
    "lessThan": "<",
    "greaterThanOrEqual": ">=",
    "lessThanOrEqual": "<=",
  };

  return (
    <div className="p-4 h-full flex flex-col">
      <h2 className="text-lg font-semibold mb-4">Filters</h2>
      <div className="space-y-4 flex-grow overflow-auto">
        {filters.map((filter) => (
          <div key={filter.id} className="p-2 border rounded-lg space-y-2">
            <div className="flex items-center space-x-2">
              <Select
                value={filter.field}
                onValueChange={(value) => updateFilter(filter.id, { field: value })}
              >
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {Object.entries(FILTERABLE_COLUMNS).map(([value, label]) => (
                    <SelectItem key={value} value={value}>{label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button variant="ghost" size="icon" onClick={() => removeFilter(filter.id)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <Select
              value={filter.operator}
              onValueChange={(value) => updateFilter(filter.id, { operator: value })}
            >
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="==">等于</SelectItem>
                <SelectItem value=">">大于</SelectItem>
                <SelectItem value="<">小于</SelectItem>
                <SelectItem value=">=">大于等于</SelectItem>
                <SelectItem value="<=">小于等于</SelectItem>
              </SelectContent>
            </Select>
            <Input
              placeholder="Value"
              value={filter.value}
              onChange={(e) => updateFilter(filter.id, { value: e.target.value })}
            />
          </div>
        ))}
      </div>
      <Button onClick={addFilter} className="mt-4">
        <PlusCircle className="mr-2 h-4 w-4" /> Add Filter
      </Button>
      <Button onClick={applyFilters} disabled={filterMutation.isPending} className="mt-2">
        {filterMutation.isPending ? "Applying..." : "Apply Filters"}
      </Button>
    </div>
  );
};

export default Sidebar;
