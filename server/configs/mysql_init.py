#table_name
table_name=["BoardAOI","WirelessAOI"]


# #table_field
# table_inits={"aoi_image":{"image_name":"VARCHAR(100)",
#                         "product_type":"VARCHAR(50)",
#                         "device_type":"VARCHAR(50)",
#                         "label":"VARCHAR(50)",
#                         "board_id":"VARCHAR(20)",
#                         "board_loc":"VARCHAR(20)",
#                         "time_point":"DATETIME"
#                         }
#             }

table_inits={"BoardAOI":{"image_name":"VARCHAR(100)",
                        "device_id":"VARCHAR(20)",
                        "time_point":"DATETIME",
                        "product_type":"VARCHAR(20)",
                        "board_id":"VARCHAR(20)",
                        "component":"VARCHAR(20)",
                        "board_loc":"VARCHAR(20)",
                        "label":"VARCHAR(5)"
                        },
            "WirelessAOI":{"image_name":"VARCHAR(80)",
                        "board_id":"VARCHAR(30)",
                        "mission_id":"VARCHAR(30)",
                        "time_point":"DATETIME",
                        "label":"VARCHAR(5)"
                        }
            }


Image_Table_Fields_Define_Detection_Segmentation={
    "Uuid":"VARCHAR(36)",
    "MachineId":"VARCHAR(100)",
    "ProjectName":"VARCHAR(100)",
    "ProductName":"VARCHAR(100)",
    "BarCode": "VARCHAR(100)",
    "ImageName": "VARCHAR(200)",
    "LabelType": "VARCHAR(100)",
    "Labels": "json",
    "GenerateDateTime":"DATETIME"
}

Image_Table_Fields_Define_Detection_Segmentation_jsonFile={
    "Uuid":"VARCHAR(36)",
    "MachineId":"VARCHAR(100)",
    "ProjectName":"VARCHAR(100)",
    "ProductName":"VARCHAR(100)",
    "BarCode": "VARCHAR(100)",
    "ImageName": "VARCHAR(200)",
    "LabelType": "VARCHAR(100)",
    "Labels": "VARCHAR(300)",
    "GenerateDateTime":"DATETIME"
}

Image_Table_Fields_Define_Classification={
    "Uuid":"VARCHAR(36)",
    "MachineId":"VARCHAR(100)",
    "ProjectName":"VARCHAR(100)",
    "ProductName":"VARCHAR(100)",
    "BarCode":"VARCHAR(100)",
    "ImageName":"VARCHAR(200)",
    "LabelType":"VARCHAR(100)",
    "ObjectType":"VARCHAR(100)",
    "ObjectName":"VARCHAR(200)",
    "label":"VARCHAR(100)",
    "GenerateDateTime":"DATETIME"
}

        