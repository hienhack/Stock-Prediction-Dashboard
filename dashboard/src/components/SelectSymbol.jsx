import { Dropdown } from "antd";
import { SYMBOL_OPTIONS } from "../config/Constant";
import { IoCaretDown } from "react-icons/io5";
import clsx from "clsx";
import { useState } from "react";

function SelectSymbol({ symbol, onChange }) {
  const [changingSymbol, setChangingSymbol] = useState(false);

  return (
    <div className="ml-4">
      <Dropdown
        menu={{
          items: SYMBOL_OPTIONS,
          selectable: true,
          onClick: (e) => onChange(e.key),
        }}
        trigger={["click"]}
      >
        <div className="flex items-center space-x-2 w-fit">
          <h1 className="text-2xl font-semibold text-slate-600 inline-block">
            {SYMBOL_OPTIONS.find((item) => item.key === symbol)?.label}
          </h1>
          <IoCaretDown
            className={clsx(
              "fill-slate-600 transition-transform duration-500 size-5",
              changingSymbol && "-rotate-180"
            )}
          />
        </div>
      </Dropdown>
    </div>
  );
}

export default SelectSymbol;
