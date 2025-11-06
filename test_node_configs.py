sample_dags = [
    {
        "use_case": "Generate Report and Schedule Review",
        "nodes": [
            {
                "id": "n1",
                "tool": "GOOGLEDOCS_CREATE_DOCUMENT",
                "inputs": {
                    "title": "Quarterly Sales Report", 
                    "text": ""
                },
            },
            {
                "id": "n2",
                "tool": "GOOGLEDRIVE_UPLOAD_FILE",
                "inputs": {
                    "file_path": "@{{n1.data.response_data.documentUrl}}",
                    "folder_id": "sales_reports_folder_id",
                },
                "depends_on": ["n1"],
            },
            {
                "id": "n3",
                "tool": "GOOGLECALENDAR_CREATE_EVENT",
                "inputs": {
                    "summary": "Sales Report Review",
                    "start_datetime": "2025-02-07T10:00:00Z",
                    "end_time": "2025-02-07T11:00:00Z",
                    "description": "Report link: @{{n2.data.response_data.webViewLink}}",
                },
                "depends_on": ["n2"],
            },
            {
                "id": "n4",
                "tool": "GMAIL_SEND_EMAIL",
                "inputs": {
                    "recipient_email": "finance_team@example.com",
                    "subject": "Report Review Scheduled",
                    "body": "Report uploaded: @{{n2.data.response_data.webViewLink}}\nMeeting scheduled: @{{n3.data.response_data.htmlLink}}",
                },
                "depends_on": ["n2", "n3"],
            },
        ],
    },
    # {
    #     "use_case": "Upload Presentation and Share Meeting Link",
    #     "nodes": [
    #         {
    #             "id": "n1",
    #             "tool": "GOOGLEDRIVE_UPLOAD_FILE",
    #             "inputs": {
    #                 "file_path": "presentation_final.pdf",
    #                 "folder_id": "client_presentations_folder_id",
    #             },
    #         },
    #         {
    #             "id": "n2",
    #             "tool": "GOOGLEMEET_CREATE_MEET",
    #             "inputs": {"title": "Client Presentation Discussion"},
    #             "depends_on": ["n1"],
    #         },
    #         {
    #             "id": "n3",
    #             "tool": "GMAIL_SEND_EMAIL",
    #             "inputs": {
    #                 "recipient_email": "client@example.com",
    #                 "subject": "Presentation & Meeting Details",
    #                 "body": "Presentation: @{{n1.data.response_data.webViewLink}}\nMeet link: @{{n2.data.response_data.meetingUri}}",
    #             },
    #             "depends_on": ["n1", "n2"],
    #         },
    #     ],
    # },
    # {
    #     "use_case": "Calendar Event Follow-up with Docs",
    #     "nodes": [
    #         {
    #             "id": "n1",
    #             "tool": "GOOGLECALENDAR_CREATE_EVENT",
    #             "inputs": {
    #                 "summary": "Post-Sprint Retrospective",
    #                 "start_datetime": "2025-03-02T15:00:00Z",
    #                 "end_time": "2025-03-02T16:00:00Z",
    #                 "description": "Discuss project improvements and blockers.",
    #             },
    #         },
    #         {
    #             "id": "n2",
    #             "tool": "GOOGLEDOCS_CREATE_DOCUMENT",
    #             "inputs": {
    #                 "title": "Sprint Retrospective Notes",
    #             },
    #             "depends_on": ["n1"],
    #         },
    #         {
    #             "id": "n3",
    #             "tool": "GMAIL_SEND_EMAIL",
    #             "inputs": {
    #                 "recipient_email": "devteam@example.com",
    #                 "subject": "Retrospective Scheduled & Notes Document",
    #                 "body": "Meeting: @{{n1.data.response_data.htmlLink}}\nNotes doc: @{{n2.data.response_data.documentUrl}}",
    #             },
    #             "depends_on": ["n1", "n2"],
    #         },
    #     ],
    # },
    # {
    #     "use_case": "Document Collaboration Setup",
    #     "nodes": [
    #         {
    #             "id": "n1",
    #             "tool": "GOOGLEDRIVE_CREATE_FOLDER",
    #             "inputs": {"name": "Collaboration Folder"},
    #         },
    #         {
    #             "id": "n2",
    #             "tool": "GOOGLEDOCS_CREATE_DOCUMENT",
    #             "inputs": {"title": "Collaboration Guidelines"},
    #             "depends_on": ["n1"],
    #         },
    #         {
    #             "id": "n3",
    #             "tool": "GMAIL_SEND_EMAIL",
    #             "inputs": {
    #                 "recipient_email": "team@example.com",
    #                 "subject": "Collaboration Folder & Doc",
    #                 "body": "Folder created: @{{n1.data.response_data.webViewLink}}\nGuidelines: @{{n2.data.response_data.documentUrl}}",
    #             },
    #             "depends_on": ["n1", "n2"],
    #         },
    #         {
    #             "id": "n4",
    #             "tool": "GOOGLECALENDAR_CREATE_EVENT",
    #             "inputs": {
    #                 "summary": "Team Collaboration Session",
    #                 "start_datetime": "2025-03-05T13:00:00Z",
    #                 "end_time": "2025-03-05T14:00:00Z",
    #                 "description": "Review guidelines: @{{n2.data.response_data.documentUrl}}",
    #             },
    #             "depends_on": ["n3"],
    #         },
    #     ],
    # },
    # {
    #     "use_case": "Prepare and Share Training Material",
    #     "nodes": [
    #         {
    #             "id": "n1",
    #             "tool": "GOOGLEDOCS_CREATE_DOCUMENT",
    #             "inputs": {"title": "Employee Training Notes"},
    #         },
    #         {
    #             "id": "n2",
    #             "tool": "GOOGLEDRIVE_UPLOAD_FILE",
    #             "inputs": {
    #                 "file_path": "@{{n1.data.response_data.documentUrl}}",
    #                 "folder_id": "training_materials_folder_id",
    #             },
    #             "depends_on": ["n1"],
    #         },
    #         {
    #             "id": "n3",
    #             "tool": "GOOGLEMEET_CREATE_MEET",
    #             "inputs": {"title": "Training Session"},
    #             "depends_on": ["n2"],
    #         },
    #         {
    #             "id": "n4",
    #             "tool": "GMAIL_SEND_EMAIL",
    #             "inputs": {
    #                 "recipient_email": "newhires@example.com",
    #                 "subject": "Training Session & Material",
    #                 "body": "Material: @{{n1.data.response_data.documentUrl}}\nMeet link: @{{n3.data.response_data.meetingUri}}",
    #             },
    #             "depends_on": ["n1", "n2", "n3"],
    #         },
    #     ],
    # },
]
