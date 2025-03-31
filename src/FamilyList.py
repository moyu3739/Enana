from Error import *
from Family import Family, MakeCommonFamilyClass

from RealEsrganNcnnVulkan import RealEsrganNcnnVulkan
# TODO: add more family


IMPLEMENTED_FAMILY_LIST = {
    RealEsrganNcnnVulkan.family_name: RealEsrganNcnnVulkan,
    # TODO: add more family
}

def GetAllFamilies() -> list[str]:
    """
    获取所有超分辨率模型系列的名称，去除重复项
    """
    local_family_set = set(Family.GetAllLocalFamilies())
    implemented_family_set = set(IMPLEMENTED_FAMILY_LIST.keys())
    all_family_set = local_family_set.union(implemented_family_set)
    return list(all_family_set)

def GetFamilyClass(family_name: str) -> type[Family]:
    """
    根据系列名称获取系列对象
    """
    if family_name not in GetAllFamilies():
        raise FamilyNotFoundError(f"Unknown family '{family_name}'.")
    return IMPLEMENTED_FAMILY_LIST.get(family_name, MakeCommonFamilyClass(family_name))

