from app.utils.output_schemas import DefaultErrorSchema

error_responses = {
    400: {"model": DefaultErrorSchema},
    404: {"model": DefaultErrorSchema},
}
