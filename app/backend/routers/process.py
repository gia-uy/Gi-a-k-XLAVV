import json
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response, JSONResponse
from services.image_io import read_image, process_via_an, encode_png
from services.contracts import normalize_steps
from services.auto_enhance import enhance,analyze
from enhancements.smart_enhance import smart_enhance

router=APIRouter(prefix='/api',tags=['Process'])

@router.post('/analyze')
async def analyze_upload(file:UploadFile=File(...)):
    image=await read_image(file)
    return {'analysis':analyze(image),'width':int(image.shape[1]),'height':int(image.shape[0])}

@router.post('/auto-enhance')
async def auto_enhance(file:UploadFile=File(...),level:str=Form('vua')):
    image=await read_image(file)
    try:
        out,metadata=enhance(image,level)
    except ValueError as exc:
        raise HTTPException(400,str(exc)) from exc
    # metadata trong header để Streamlit/Frontend đọc; ảnh là PNG thuần.
    return Response(content=encode_png(out),media_type='image/png',
                    headers={'X-Processing-Metadata':json.dumps(metadata,ensure_ascii=True),
                             'Access-Control-Expose-Headers':'X-Processing-Metadata'})

@router.post('/process')
async def process(file:UploadFile=File(...), steps:str=Form('[]')):
    parsed=normalize_steps(steps)
    image=await read_image(file)
    result=process_via_an(image,parsed)
    return Response(content=encode_png(result),media_type='image/png')


@router.post('/smart-enhance')
async def smart_enhance_upload(file: UploadFile = File(...)):
    # Đọc ảnh bằng hàm có sẵn của backend
    image = await read_image(file)

    try:
        # Gọi thuật toán riêng của bạn
        result, metadata = smart_enhance(image)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    # Trả ảnh PNG và metadata giống auto-enhance
    return Response(
        content=encode_png(result),
        media_type='image/png',
        headers={
            'X-Processing-Metadata': json.dumps(
                metadata,
                ensure_ascii=True
            ),
            'Access-Control-Expose-Headers':
                'X-Processing-Metadata'
        }
    )
