export default function reducer(state={
    list:[],
    measurement_list:[],
    device_data: {
        data: [],
    },
    measurement_data:{
        data:[],
    }


},action){
    switch (action.type) {
        case "MODEL_GET_MODEL_LIST":
            return{
                ...state,
                list:action.payload
            }
        case "MODEL_GET_MEASUREMENT_LIST":
            return {
                ...state,
                measurement_list:action.payload
            }
        case "MODEL_GET_MEASUREMENT_DATA":
            return {
                ...state,
                measurement_data:action.payload
            }
        case "MODEL_DEVICE_DATA":
            return{
                ...state,
                device_data:action.payload
            }
        default:
            return state;
    }
}

