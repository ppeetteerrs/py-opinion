from collections import UserDict
from typing import Any, Dict, Generic, List, Tuple, TypeVar, Union, overload

import numpy as np
import pandas as pd
from typing_extensions import TypeVarTuple, Unpack

K = TypeVar("K")
KT = TypeVarTuple("KT")
VT = TypeVar("VT")


class MIDict(UserDict, Generic[K, Unpack[KT], VT]):  # type: ignore
    def __init__(
        self,
        data: Dict[Tuple[K, Unpack[KT]], VT],
    ):
        assert len(data) > 0, "Data dictionary cannot be empty!"
        self.key_map = pd.Series(
            range(len(data)), index=pd.MultiIndex.from_tuples(data.keys()), dtype=int
        )
        self.key_map.sort_index(ascending=True, inplace=True)
        self.data: Dict[int, VT] = {i: v for i, v in enumerate(data.values())}
        self.__secret_count = len(data)

    def __setitem__(
        self,
        args: Tuple[Union[slice, Unpack[KT], List[Union[Unpack[KT]]]], ...],
        val: VT,
    ):
        self.key_map.loc[args] = self.__secret_count  # type: ignore
        self.data[self.__secret_count] = val
        self.__secret_count += 1
        self.key_map.sort_index(ascending=True, inplace=True)

    @overload
    def __getitem__(
        self, args: K
    ) -> Dict[Union[Tuple[Unpack[KT]], Union[Unpack[KT]]], VT]:  # pragma: no cover
        ...

    @overload
    def __getitem__(
        self, args: List[K]
    ) -> Dict[Tuple[K, Unpack[KT]], VT]:  # pragma: no cover
        ...

    @overload
    def __getitem__(self, args: Tuple[K, Unpack[KT]]) -> VT:  # type: ignore # pragma: no cover
        ...

    @overload
    def __getitem__(
        self, args: slice
    ) -> Dict[Tuple[K, Unpack[KT]], VT]:  # pragma: no cover
        ...

    @overload
    def __getitem__(
        self, args: Tuple[Union[slice, List[Union[K, Unpack[KT]]]], ...]
    ) -> Dict[Tuple[K, Unpack[KT]], VT]:  # pragma: no cover
        ...

    @overload
    def __getitem__(
        self, args: Tuple[Union[slice, K, Unpack[KT], List[Union[K, Unpack[KT]]]], ...]
    ) -> Dict[Any, VT]:  # pragma: no cover
        ...

    def __getitem__(self, args: Any) -> Any:  # type: ignore
        keys = self.key_map.loc[args]
        if isinstance(keys, pd.Series):  # type: ignore
            return {k: self.data[v] for k, v in keys.to_dict().items()}
        else:
            return self.data[keys]

    def __delitem__(
        self, args: Tuple[Union[slice, Unpack[KT], List[Union[Unpack[KT]]]], ...]
    ):
        self.key_map.loc[args] = np.nan  # type: ignore
        self.key_map = self.key_map.dropna()
        self.data = {k: self.data[k] for k in self.key_map.unique()}
