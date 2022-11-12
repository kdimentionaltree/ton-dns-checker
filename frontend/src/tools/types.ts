import { GridProps } from "@mui/material";

export type DataType = {
  idx: number;
  ip: string;
  ip_int: number;
  port: number;
  key: string;
  is_online: boolean;
};
export type DHTDataType = {
  idx: number;
  ip: string;
  ip_int: number;
  port: number;
  key: string;
  is_online: boolean;
};
export type LSDataType = {
  idx: number;
  ip: string;
  ip_int: number;
  port: number;
  key: string;
  is_online: boolean;
};

export type SearchProps = {
  value: string;
  onSearch: (value: string) => void;
};

export type DataGridProps = {
  dhtData: DHTDataGridProps;
  lsData: LSDataGridProps;
  selectedTable: "DHT" | "LS";
  setSelectedTable: (value: "DHT" | "LS") => void;
  disabled: boolean;
};

export type DHTResolvedType = {
  ip: string | null;
  port: number | null;
};
export type DHTDataGridProps = {
  data: DHTDataType[];
  resolved: DHTResolvedType[];
  isLoading: boolean;
};
export type DHTDataGridItemProps = {
  item: DHTDataType;
  resolved: DHTResolvedType | null;
  isLoading: boolean;
};
export type DataGridItemProps = GridProps & {
  data: any;
  needMeta: boolean;
  isOnline?: boolean;
};

export type LSResolvedType = {
  adnl: string | null;
};
export type LSDataGridProps = {
  data: LSDataType[];
  resolved: LSResolvedType[];
  isLoading: boolean;
};
export type LSataGridItemProps = {
  item: LSDataType;
  resolved: LSResolvedType | null;
  isLoading: boolean;
};
export type AdvancedGridItemProps = GridProps & {
  label?: string;
  content: any;
  isLink?: boolean;
};
