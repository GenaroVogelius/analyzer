import { Checkbox } from "@/components/ui/checkbox";
import { FormatNumberColor } from "@/hooks/useFormatNumberColor";
import { createColumnHelper } from "@tanstack/react-table";
import { ColumnHeaderSorted } from "../../../components/Columns/Components/Columns/ColumnHeaderSorted/ColumnHeaderSorted";
import { DragHandler } from "../../../components/Columns/Components/DragHandler/DragHandler";

export type PositionsColumnsType = {
  id: number;
  ticker: string;
  amount: number;
  date_operation: string;
  date_liquidation: string;
  buy_price: number;
  sell_price: number;
  inverted_amount: number;
  current_amount: number;
  percentage_gain: number;
  nominal_gain: number;
  tna: number;
};

const columnHelper = createColumnHelper<PositionsColumnsType>();

export const PositionsColumns = [
  columnHelper.display({
    id: "drag",
    header: () => null,
    cell: ({ row }) => <DragHandler id={row.original.id} />,
  }),
  columnHelper.display({
    id: "select",
    header: ({ table }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && "indeterminate")
          }
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      </div>
    ),
    cell: ({ row }) => (
      <div className="flex items-center justify-center">
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
  }),
  columnHelper.accessor("ticker", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Ticket"
        tooltipContent="Ticket"
      />
    ),
    cell: ({ getValue }) => {
      return <span>{getValue()}</span>;
    },
  }),
  columnHelper.accessor("buy_price", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Buy Price"
        tooltipContent="Buy price"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("sell_price", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Sell Price"
        tooltipContent="Sell price"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("inverted_amount", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Inverted Amount"
        tooltipContent="Inverted amount"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("amount", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Amount"
        tooltipContent="Amount"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("percentage_gain", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Percentage Gain"
        tooltipContent="Percentage gain"
      />
    ),
    cell: ({ getValue }) => <div className="">{getValue()}</div>,
    sortingFn: "basic",
  }),
  columnHelper.accessor("nominal_gain", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="Nominal Gain"
        tooltipContent="Nominal gain"
      />
    ),
    cell: ({ getValue }) => {
      const { displayValue, className } = FormatNumberColor(getValue(), { isBeforeValue: true, sign: "$" }, 0, true);
      return <div className={className}>{displayValue}</div>;
    },
    sortingFn: "basic",
  }),
  columnHelper.accessor("tna", {
    header: ({ column }) => (
      <ColumnHeaderSorted
        column={column}
        title="TNA"
        tooltipContent="Annual nominal rate"
      />
    ),
    cell: ({ getValue }) => {
      const { displayValue, className } = FormatNumberColor(getValue(), { isBeforeValue: false, sign: "%" }, 0, true);
      return <div className={className}>{displayValue}</div>;
    },
    sortingFn: "basic",
  }),
];
