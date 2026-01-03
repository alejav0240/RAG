from pydantic import BaseModel, Field

class AnalisisCV(BaseModel):
    """
    Modelo que representa el analisis de un CV
    """
    nombre_candidato: str = Field(..., description="Nombre completo del candidato extraido del cv")
    experiencia_laboral: int = Field(..., description="Experiencia laboral relevante extraida del cv")
    habilidades_clave: list[str] = Field(..., description="Lista de las 5 - 7 habilidades clave extraidas del cv")
    educacion: str = Field(..., description="Nivel educativoo mas alto y especializacion principal extraida del cv")
    experiencia_relevante: str = Field(..., description="Resumen breve de la experiencia laboral relevante extraida del cv")
    fortalezas: list[str] = Field(..., description="Lista de las 5 - 7 fortalezas extraidas del cv")
    areas_mejora: list[str] = Field(..., description="Lista de las 2 - 4 areas donde el candiadto podria desarrollarse o mejorar")
    porcentaje_ajuste: int = Field(..., description="Porcentaje de ajuste entre el perfil del candidato y el perfil del puesto",ge=0, le=100)